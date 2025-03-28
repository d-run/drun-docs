# Manage Your API Keys

API keys are essential credentials for accessing model services. They are used to authenticate your identity and ensure the security of your data.

![api keys](./images/apikey01.png)

## Overview

- **What is an API Key?**

    - An API key is a required credential for calling model services. It verifies your identity and allows secure access to deployed services.
    - With your API key, you can make secure requests to the model services.

- **Security Tips:**

    - Keep your API key safe and avoid exposing it in client-side code or public environments.
    - If your API key is compromised, delete it immediately and generate a new one.

## Creating an API Key

1. Navigate to the **API Keys** page and click the **Create** button in the top-right corner.
2. In the pop-up window, enter a name for your API key (e.g., "test-key") to indicate its purpose or associated project.
3. Click **OK** . The system will generate a new API key for you.

!!! note

    Be sure to save your API key when it's first shown, as it will not be displayed again.

## Viewing API Keys

- The API key list shows all your created keys:

    - **Name:** The name you assigned to the API key, helping you identify its purpose.
    - **API Key:** A partial view of the key for reference.
    - **Creation Time:** The date and time when the API key was created.

- To refresh the list, click the refresh :material-refresh: button in the top-right corner.

## Deleting an API Key

1. Find the API key you want to delete from the list.
2. Click the row to initiate the delete action.
3. Confirm the deletion in the pop-up window.
4. Once deleted, the API key becomes invalid, and all requests using that key will be rejected.

## Using an API Key to Call Services

When making requests to model services, include the following field in your HTTP request header:

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

## Important Notes

- **API Key Limit:** Each account can create a limited number of API keys. Please manage them wisely.
- **Handling Key Leaks:** If your key is compromised, immediately delete the old key and generate a new one.
- **Key Permissions:** Different API keys can be used for separate projects or services, making it easy to manage permissions.
- **Regularly Update Keys:** For security, it's recommended to periodically delete old keys and generate new ones.
