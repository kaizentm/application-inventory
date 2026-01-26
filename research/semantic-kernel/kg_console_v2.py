# TODO: look at graphdb / rdf mcp servers
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from SPARQLWrapper import SPARQLWrapper, JSON

load_dotenv()

# Configuration
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("DEPLOYMENT_NAME")
system_message_file = os.getenv("SYSTEM_MESSAGE_FILE", "app-inventory-prompt.txt")
graphdb_repository = os.getenv("GRAPHDB_REPOSITORY")

# Setup SPARQL
sparql = SPARQLWrapper(graphdb_repository)

def query_graphdb(query: str) -> str:
    """Queries the graph database with SPARQL."""
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    ret = sparql.queryAndConvert()
    print(f"\n[SPARQL Query]\n{query}\n")
    results = ret["results"]["bindings"]
    return json.dumps(results, indent=2)

# Define the tool for function calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_graphdb",
            "description": "Queries the graph database using SPARQL to retrieve information about applications, their dependencies, and relationships.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A valid SPARQL query to execute against the graph database"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def process_tool_calls(response, messages):
    """Process any tool calls in the response."""
    while response.choices[0].message.tool_calls:
        tool_calls = response.choices[0].message.tool_calls
        
        # Add assistant message with tool calls
        messages.append(response.choices[0].message)
        
        # Process each tool call
        for tool_call in tool_calls:
            if tool_call.function.name == "query_graphdb":
                args = json.loads(tool_call.function.arguments)
                result = query_graphdb(args["query"])
                
                # Add tool response
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        
        # Get next response
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
    
    return response

# Setup Azure OpenAI client with new v1 API
print("Initializing OpenAI client (Azure v1 API)...")
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

# New v1 API: Use OpenAI client with base_url including /openai/v1/
# No need to specify api_version anymore
base_url = endpoint.rstrip('/') + "/openai/v1/"

client = OpenAI(
    base_url=base_url,
    api_key=token_provider,
)

# Load system message
with open(system_message_file, 'r') as file:
    system_message = file.read()

# Initialize chat history
messages = [{"role": "system", "content": system_message}]

print(f"Connected to: {endpoint}")
print(f"Deployment: {deployment}")
print(f"GraphDB: {graphdb_repository}")
print("\nReady! Type 'exit' to quit.\n")

# Chat loop
while True:
    user_input = input("User > ")
    
    if user_input.lower() == "exit":
        break
    
    if not user_input.strip():
        continue
    
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        
        # Process any tool calls
        response = process_tool_calls(response, messages)
        
        # Get final response
        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        
        print(f"Assistant > {assistant_message}\n")
        
    except Exception as e:
        print(f"Error: {e}\n")

print("Goodbye!")
client.close()
