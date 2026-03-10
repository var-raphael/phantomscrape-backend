from flask import Flask
from flask cors import CORS
from routes import api

app = Flask(__name__)
CORS(app)

app.register_blueprint(api)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)