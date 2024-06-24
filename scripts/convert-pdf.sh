#!/bin/bash

# 检查是否提供了目录
if [ -z "$1" ]; then
  echo "请提供包含 Markdown 文件的目录。"
  exit 1
fi

# 获取目录路径
input_dir="$1"

# 创建一个输出目录
output_dir="${input_dir}/pdf_output"
mkdir -p "$output_dir"

# 初始化一个数组来存储生成的 PDF 文件路径
pdf_files=()

# 遍历目录中的所有 Markdown 文件
for file in "$input_dir"/*.md; do
  if [ -f "$file" ]; then
    # 获取文件名（不带扩展名）
    filename=$(basename -- "$file")
    filename="${filename%.*}"
    # 转换为 PDF
    output_pdf="${output_dir}/${filename}.pdf"
    pandoc "$file" -o "$output_pdf"
    echo "已将 $file 转换为 $output_pdf"
    # 将生成的 PDF 文件路径添加到数组中
    pdf_files+=("$output_pdf")
  fi
done

# 合并所有 PDF 文件
merged_pdf="${output_dir}/merged_output.pdf"
pdfunite "${pdf_files[@]}" "$merged_pdf"

echo "所有文件已转换并合并为 $merged_pdf"