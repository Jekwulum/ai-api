from dotenv import load_dotenv
from flask import Flask, jsonify
from app.routes import routes

load_dotenv()

port = 5600
app = Flask(__name__)
app.register_blueprint(routes)

@app.route('/health', methods=['GET'])
def health_check():
	return jsonify({"status": "Healthy ✅"}), 200


def start_app():
	app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
	start_app()