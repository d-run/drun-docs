import requests
import json
import csv
from datetime import datetime, timezone
import pandas as pd
from collections import OrderedDict
import yaml
import re
import logging
import os




# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

ITEM_HEADER = [
    '功能模块',
    '发布版本',
    '发版时间',
    '更新类型',
    '一级功能',
    '二级功能',
    '基线参数'
]

def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    payload = {"app_id": app_id, "app_secret": app_secret}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        token = data.get("tenant_access_token")
        if not token:
            logging.error("获取tenant_access_token失败，响应内容: %s", data)
            return None
        return token
    except requests.RequestException as e:
        logging.error("请求tenant_access_token失败: %s", e)
        return None

def get_node_info(node_token, tenant_access_token):
    url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node"
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    params = {"token": node_token, "obj_type": "wiki"}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        logging.error("请求node_info失败: %s", e)
        return None

def get_sheet_content(app_token, table_id, view_id, tenant_access_token, page_size=100, page_token=None):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "view_id": view_id,
        "page_size": page_size,
    }
    if page_token:
        payload["page_token"] = page_token
    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        logging.error("请求sheet_content失败: %s", e)
        return None

def get_items(data):
    if not data or 'data' not in data or 'items' not in data['data']:
        logging.warning("数据格式错误或无items字段")
        return [ITEM_HEADER]
    items = data['data']['items']
    filter_items = [ITEM_HEADER]
    for item in items:
        fields = item.get('fields', {})
        first_level = ','.join([x.get('text', '') for x in fields.get('一级功能', [])]) if fields.get('一级功能') else ''
        second_level = ','.join([x.get('text', '') for x in fields.get('二级功能', [])]) if fields.get('二级功能') else ''
        baseline = ','.join([x.get('text', '') for x in fields.get('基线参数', [])]) if fields.get('基线参数') else ''
        version = ''
        if fields.get('版本') and fields['版本'].get('value'):
            try:
                version = fields['版本']['value'][0].get('text', '')
            except (IndexError, AttributeError):
                version = ''
        release_time = fields.get('发版时间', {})
        normal_date = None
        if release_time and 'value' in release_time and release_time['value']:
            try:
                timestamp = int(release_time['value'][0]) / 1000
                normal_date = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d')
            except (ValueError, IndexError, TypeError):
                normal_date = None
        row = [
            fields.get('功能模块', ''),
            version,
            normal_date,
            fields.get('更新类型', ''),
            first_level,
            second_level,
            baseline
        ]
        if version:
            filter_items.append(row)
    return filter_items

def get_release_Dict(data):
    if not data or len(data) < 2:
        logging.warning("数据不足，无法生成release字典")
        return OrderedDict()
    df = pd.DataFrame(data[1:], columns=data[0])
    def version_key(v):
        try:
            parts = v.lstrip('v').split('.')
            return tuple(int(x) for x in parts)
        except Exception:
            return (0,)
    df['版本排序'] = df['发布版本'].apply(version_key)
    module_order = {'算力云': 0, '大模型服务平台': 1, '费用中心': 2, '用户中心': 3}
    update_type_order = {'新功能': 0, '增强优化': 1, '故障修复': 2, '无更新类型': 3}
    df['更新类型'] = df['更新类型'].replace({'': '无更新类型'})
    df['功能模块排序'] = df['功能模块'].map(module_order).fillna(99)
    df['更新类型排序'] = df['更新类型'].map(update_type_order).fillna(99)
    df_sorted = df.sort_values(by=['发版时间', '功能模块排序', '版本排序', '更新类型排序', '一级功能'],
                               ascending=[False, True, True, True, True])
    result = OrderedDict()
    for _, row in df_sorted.iterrows():
        pub_date = row['发版时间']
        module = row['功能模块']
        version = row['发布版本']
        update_type = row['更新类型']
        primary_func = row['一级功能']
        entry = {
            '二级功能': row['二级功能'],
            '基线参数': row['基线参数']
        }
        result.setdefault(pub_date, OrderedDict()) \
              .setdefault(module, OrderedDict()) \
              .setdefault(version, OrderedDict()) \
              .setdefault(update_type, []).append((primary_func, entry))
    # 组内一级功能排序
    for pub_date in result:
        for module in result[pub_date]:
            for version in result[pub_date][module]:
                for update_type in result[pub_date][module][version]:
                    result[pub_date][module][version][update_type].sort(key=lambda x: x[0])
    return result

def get_release_info(data, filename='rel-notes.md'):
    items = get_items(data)
    result = get_release_Dict(items)
    from string import Template

    emoji_map = {
        '新功能': '🚀 新功能',
        '增强优化': '⚡ 增强优化',
        '故障修复': '🐛 故障修复',
        '无更新类型': ''
    }

    # 定义模板
    header_template = Template('''---
hide:
- toc
---

# Release Notes

本页列出 d.run 各项功能的一些重要变更。

    ''')

    pub_date_template = Template('## $pub_date\n\n')
    module_version_template = Template('### $module $version\n\n')
    update_type_template = Template('#### $emoji_title\n\n')
    entry_with_baseline_template = Template('- [$primary_func] $baseline')
    entry_without_baseline_template = Template('- [$primary_func]')

    lines = []
    lines.append(header_template.substitute())

    for pub_date, modules in result.items():
        lines.append(pub_date_template.substitute(pub_date=pub_date))
        for module, versions in modules.items():
            for version, update_types in versions.items():
                lines.append(module_version_template.substitute(module=module, version=version))
                for update_type in ['新功能', '增强优化', '故障修复', '无更新类型']:
                    if update_type in update_types:
                        entries = update_types[update_type]
                        if update_type != '无更新类型':
                            lines.append(update_type_template.substitute(emoji_title=emoji_map[update_type]))
                        for primary_func, entry in entries:
                            baseline = entry.get('基线参数', '')
                            if baseline:
                                lines.append(entry_with_baseline_template.substitute(primary_func=primary_func, baseline=baseline))
                            else:
                                lines.append(entry_without_baseline_template.substitute(primary_func=primary_func))
                        lines.append('')  # 空行分隔

    md_content = '\n'.join(lines)
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        logging.info("Release notes已保存到 %s", filename)
    except Exception as e:
        logging.error("写入release notes文件失败: %s", e)

def parse_feishu_url(url):
    node_token = None
    table_id = None
    view_id = None
    if not url:
        return node_token, table_id, view_id
    match_node = re.search(r'/wiki/([^/?]+)', url)
    if match_node:
        node_token = match_node.group(1)
    match_table = re.search(r'table=([^&]+)', url)
    if match_table:
        table_id = match_table.group(1)
    match_view = re.search(r'view=([^&]+)', url)
    if match_view:
        view_id = match_view.group(1)
    return node_token, table_id, view_id

if __name__ == "__main__":
    file_out_name = os.environ.get("FILENAME")
    app_id = os.environ.get("APP_ID")
    app_secret = os.environ.get("APP_SECRET")
    url = os.environ.get("URL")
    
    node_token, table_id, view_id = parse_feishu_url(url) if url else (None, None, None)
    if not all([app_id, app_secret, node_token, table_id, view_id]):
        logging.error("配置信息不完整，程序退出")
        exit(1)

    tenant_access_token = get_tenant_access_token(app_id, app_secret)
    if not tenant_access_token:
        logging.error("获取tenant_access_token失败，程序退出")
        exit(1)

    node_info = get_node_info(node_token, tenant_access_token)
    if not node_info or 'data' not in node_info or 'node' not in node_info['data']:
        logging.error("获取node_info失败，程序退出")
        exit(1)
    app_token = node_info["data"]["node"].get("obj_token")
    if not app_token:
        logging.error("obj_token缺失，程序退出")
        exit(1)

    ori_data = get_sheet_content(app_token, table_id, view_id, tenant_access_token)
    if not ori_data:
        logging.error("获取表格内容失败，程序退出")
        exit(1)
    get_release_info(ori_data, filename=file_out_name)
