import os, requests, uuid, json, config, tools
from openai import AzureOpenAI

openai_client = AzureOpenAI(
    azure_endpoint = config.openai_endpoint, 
    api_key=config.openai_key,  
    api_version="2024-08-01-preview"
)

def get_openai_response(chat_history=[],agent=None):

    headers = {
        "Content-Type": "application/json",
        "api-key": config.openai_key,
    }

    payload = {
    "messages": chat_history,
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 800,
    "tools": agent['tools']
    }

    # Send request
    try:
        response = openai_client.chat.completions.create(
            model = "gpt-4o",
            messages = chat_history,
            tools = agent['tools'],
            tool_choice = "auto"
            )
        
        response_message = response.choices[0].message
        chat_history.append(response_message)

        #response = requests.post(config.openai_endpoint, headers=headers, json=payload)
        
        print(response.json())

        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                print(function_args)
                tool_response = {}
                if function_name == "searchusermanual":
                    tool_response = tools.searchusermanual(function_args)
                elif function_name == "searchknowledgebase":
                    tool_response = tools.searchknowledgebase(function_args)
                elif function_name == "getweatherforecast":
                    tool_response = tools.getweatherforecast(function_args)
                elif function_name == "get_current_time":
                    tool_response = tools.getcurrenttime(function_args)
                
                chat_history.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": json.dumps(tool_response),
                })
                
                print("chat_history before tool response:")
                print(chat_history)

                final_response = openai_client.chat.completions.create(
                    model = "gpt-4o",
                    messages = chat_history
                )
                print("final response:")
                print(final_response)

                response_message = final_response.choices[0].message           

    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Handle the response as needed (e.g., print or process)
    return(response.json())

# Example usage:
# print(get_openai_response()['choices'][0]['message']['content'])

def get_promptflow_response(requestbody):

    endpoint = "https://tv-copilot.swedencentral.inference.ml.azure.com/score"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + config.promptflow_key,
        "azureml-model-deployment":config.promptflow_deployment
    }

    payload = requestbody
    # Send request
    try:
        response = requests.post(config.promptflow_endpoint, headers=headers, json=payload)
        print(response.json())
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Handle the response as needed (e.g., print or process)
    return(response.json())