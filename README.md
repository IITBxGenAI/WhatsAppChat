# WhatsAppChat
A proof of concept notebook of WhatsApp Q&amp;A Chat using LangChain and OpenAI


## Set-Up:

1. Create a .env file in the root of this project with the following variable:

```
OPENAI_API_KEY='your_openai_api_key'
```

Refer: https://www.maisieai.com/help/how-to-get-an-openai-api-key-for-chatgpt for any help to set up OpenAI API key.

2. To chat with the WhatsApp Group via the system, you'll need to export the group data. Open the desired WhatsApp Group, tap on the three dots -> More -> Export Chat -> Without Media.

3. Export the chat history as a .txt file and rename it to `chat_history.txt`. Then, create a `data` folder in the root of the project if it doesn't exist and place the file inside it.


## Usage:

Use the `WhatsAppChat_LangChain.ipynb` notebook to chat with the WhatsApp Group.

