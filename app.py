import os
from flask import Flask, jsonify
from flasgger import Swagger
from models import db
from auth import auth_bp
from reports import reports_bp

DB_URI = os.environ.get('DB_URI', 'localhost:8432')
DB_USER = os.environ.get('DB_USER', 'dbuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URI}/workclock-db'
app.register_blueprint(auth_bp)
app.register_blueprint(reports_bp)

swagger = Swagger(app)
db.init_app(app)

@app.route('/heartbeat')
def heartbeat():
    """
    Endpoint for checking the heartbeat of the service.

    This endpoint returns a simple 'Hello World!' message.
    ---
    responses:
      200:
        description: A successful heartbeat response.
        content:
          application/json:
            schema:
              type: object
              properties:
                Hello:
                  type: string
    """
    return jsonify({'Hello': 'World!'})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
    #with app.app_context():
    #    db.create_all()
