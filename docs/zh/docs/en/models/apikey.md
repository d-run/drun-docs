# API Key Management

API Key is the core credential for calling model services, used to verify user identity and protect data security.

## Description

- Purpose of API Key:

    - API Key is a necessary credential for calling model services, used for identity verification.
    - With the API Key, you can securely call deployed model services.

- Security Tips:

    - Please keep the API Key safe and avoid exposing it in client code or public environments.
    - If the API Key is leaked, please delete it promptly and regenerate a new Key.

## Creating an API Key

1. On the **API Key Management** page, click the **Create** button at the top right corner.
2. In the pop-up window, fill in the name of the API Key (e.g., test-key) to identify its purpose or associated project.
3. Click **OK**, and the system will generate a new API Key.

!!! note

    After creation, please save the API Key when it is first displayed, as the complete key will not be shown again.

## Viewing API Keys

- The API Key list will display all created API Keys:
    - Name: The identifying name for the API Key, helping users differentiate between Keys for different purposes.
    - API Key: Partially displays the key content, for reference only.
    - Creation Time: The time the API Key was generated.
- Click the refresh button at the top right corner to update the Key list.

## Deleting an API Key

1. Find the API Key you wish to delete in the list.
2. Click the row to perform the delete operation.
3. Confirm the delete operation in the pop-up window.
4. After deletion, the API Key will immediately become invalid, and all service calls relying on this Key will be rejected.

## Using API Key to Call Services

When calling model services, you need to add the following field in the HTTP request header:

```http
Authorization: Bearer {API_KEY}
```

Example:

```shell
curl 'https://sh-02.d.run/v1/chat/completions' \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-x1VDTAFB7Ra1hldATbncOa_dddVttDvRHQibTA-Oi7ucU" \
  -d '{
    "model": "u-8105f7322477/test",
    "messages": [{"role": "user", "content": "Hello, model!"}],
    "temperature": 0.7
  }'
```

## Notes

- API Key Quantity Limit: Each account is allowed to create a limited number of API Keys, please allocate them reasonably as needed.
- Key Leak Handling: If you discover a key leak, please immediately delete the old key and recreate a new key.
- Key Permission Management: Different API Keys can be used for different projects or services, facilitating permission isolation.
- Regularly Update Keys: For security reasons, it is recommended to periodically delete old Keys and generate new Keys.
