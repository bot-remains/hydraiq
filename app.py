from flask import Flask, jsonify, request, Response
import bs4
from langchain_community.document_loaders import WebBaseLoader
from flask_cors import CORS

from chatbot.chat_utils import fetchChatHistory, chatWithChain
from chatbot.download_files import download_s3_bucket
from chatbot.access_files import get_files
from data_setup.llm_extract import do_the_thing

app = Flask(__name__)
CORS(app)

@app.route("/scrape")
def scrape():
    loader = WebBaseLoader(web_paths=[url])
    docs = []
    for doc in loader.lazy_load():
        docs.append(doc)
    return Response(docs,)

@app.route("/chat/prepare-dataset")
def prepare():
    # download_s3_bucket("abhi-bhingradiya-pvt", "./input")
    files = get_files()
    do_the_thing(files)
    return jsonify({'message': 'Dataset prepared successfully'})

@app.route("/chat/<session_id>", methods = ['GET', 'POST'])
def disp(session_id):
    input = request.get_json(force=True)
    user_id = input.get('user_id')
    user_input = input.get('user_input')

    if not input:
        return jsonify({'error': 'No user input provided'}), 400

    chat_history = fetchChatHistory(user_id, session_id)
    return Response(chatWithChain(user_input, chat_history), content_type='text/plain')


@app.route("/chat/get-history/<session_id>", methods=['GET', 'POST'])
def hist(session_id):
    input = request.get_json(force=True)
    user_id = input.get('user_id')

    if not input:
        return jsonify({'error': 'No user input provided'}), 400

    chat_history = fetchChatHistory(user_id, session_id)
    # print(vars(chat_history.messages[0]))


    # Convert HumanMessage objects to a JSON-serializable format
    messages = [{"role": msg.type, "content": msg.content} for msg in chat_history.messages]

    return jsonify(messages)


if __name__ == '__main__':
    app.run(debug = True)