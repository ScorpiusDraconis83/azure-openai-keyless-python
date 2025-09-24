import logging
import os

import azure.identity
import openai
from dotenv import load_dotenv

load_dotenv()
# Change to logging.DEBUG for more verbose logging from Azure and OpenAI SDKs
logging.basicConfig(level=logging.WARNING)


if not os.getenv("AZURE_OPENAI_SERVICE") or not os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"):
    logging.warning("AZURE_OPENAI_SERVICE and AZURE_OPENAI_GPT_DEPLOYMENT environment variables are empty. See README.")
    exit(1)


# Change this to AzureCliCredential, DefaultAzureCredential, or another credential type if needed
credential = azure.identity.AzureDeveloperCliCredential(tenant_id=os.environ["AZURE_TENANT_ID"])
token_provider = azure.identity.get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

client = openai.OpenAI(
    base_url=f"https://{os.environ['AZURE_OPENAI_SERVICE']}.openai.azure.com/openai/v1",
    api_key=token_provider,
)

response = client.chat.completions.create(
    # For Azure OpenAI, the model parameter must be set to the deployment name
    model=os.environ["AZURE_OPENAI_GPT_DEPLOYMENT"],
    temperature=0.7,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that makes lots of cat references and uses emojis."},
        {"role": "user", "content": "Write a haiku about a hungry cat who wants tuna"},
    ],
)

print("Response: ")
print(response.choices[0].message.content)
