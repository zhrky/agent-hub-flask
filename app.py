import os, azureopenai, config, agents, tools
from flask import Flask, render_template, session, url_for, jsonify, request, send_from_directory

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = 'BAD_SECRET_KEY'


mysession ={}

@app.route('/hub')
def intro():
    return render_template('intro.html', agents=agents.agents) 

@app.route('/chat/<copilotname>')
def chat(copilotname):
    agent = next((x for x in agents.agents if x['id'] == copilotname), agents.default_agent)
    mysession['agent'] = agent
    mysession['chathistory'] = [{
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": agents.default_agent['system_prompt']
            }
        ]
    }]
    return render_template('chat.html', agent=agent, config=config) 

@app.route('/')
def index():
    mode = request.args.get('mode')
    if mode == "promptflow":
        mysession['requestbody'] = {
            "question": "",
            "chat_history": [
            ]
        }
    else:
        mysession['chathistory'] = [{
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": config.system_prompt
                }
            ]
        }]
    return render_template('index.html', mode=mode, config=config) 

@app.route('/generateold', methods=['POST'])
def generate_response():
   
    data = request.get_json()
    message_input = data['text']
    mysession['chathistory'].append(
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": message_input
            }
        ]
        }
    )
    response = azureopenai.get_openai_response(mysession['chathistory'])
    return jsonify(response)

# @app.route('/tools/<toolname>', methods=['POST'])
# def call_tools(toolname):
#     data = request.get_json()
#     if toolname == "searchusermanual":
#         response = tools.searchusermanual(data)
#     elif toolname == "searchknowledgebase":
#         response = tools.searchknowledgebase(data)
#     elif toolname == "getweatherforecast":
#         response = tools.getweatherforecast(data)
#     elif toolname == "get_current_time":
#         response = tools.getcurrenttime(data)
#     return response

@app.route('/generate', methods=['POST'])
def call_openai():
    print(mysession)
    agent = mysession['agent']
    data = request.get_json()
    message_input = data['text']
    mysession['chathistory'].append(
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": message_input
            }
        ]
        }
    )
    response = azureopenai.get_openai_response(mysession['chathistory'],agent=agent)
    return jsonify(response)


@app.route('/callpromptflow', methods=['POST'])
def call_promptflow():
	data = request.get_json()
	message_input = data['text']
	mysession['requestbody']['question'] = message_input
	print(mysession['requestbody'])
	response = azureopenai.get_promptflow_response(mysession['requestbody'])

	mysession['requestbody']['chat_history'].append(
                {
                    "inputs": {"question": message_input},
                    "outputs": {"answer": response['answer']}
                }
    )
	
	return jsonify(response)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

