import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv("../.env")

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("DEPLOYMENT_NAME")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

print(f"Endpoint: {endpoint}")
print(f"Deployment: {deployment}")
print(f"API Key: {'set' if api_key else 'not set (using Azure AD)'}")

# Use Azure AD authentication
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
)

print("\nSending request...")

response = client.chat.completions.create(
    stream=True,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "Say hello in one sentence.",
        }
    ],
    max_completion_tokens=100,
    temperature=1.0,
    model=deployment,
)

print("Response: ", end="")
for update in response:
    if update.choices:
        print(update.choices[0].delta.content or "", end="")

print("\n\nDone!")
client.close()
