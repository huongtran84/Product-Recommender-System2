from flask import Flask, request, render_template, Response
from prometheus_client import Counter, generate_latest

from flipkart.data_ingestion import DataIngestor
from flipkart.rag_chain import RAGChainBuilder
from dotenv import load_dotenv

load_dotenv()
REQUEST_COUNT = Counter('http_request_total', 'Total http requests')
def create_app():
    app = Flask(__name__)
    vector_store = DataIngestor().ingest(load_existing=True)
    rag_chain = RAGChainBuilder(vector_store).build_chain()
    @app.route('/')
    def index():
        REQUEST_COUNT.inc()
        return render_template('index.html')

    @app.route('/get', methods=['POST'])
    def get_response():
        user_input = request.form['msg']
        session_id = request.form.get('session_id', 'default_session')
        response = rag_chain.invoke({"input": user_input},config= {"configurable":{"session_id": session_id}} )['answer']
        return response
    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype='text/plain')   
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0",port=8000, debug=True)