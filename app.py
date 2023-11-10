from flask import Flask, jsonify
from models import db
from auth import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:postgres@workclock-db:5432/image-metadata'
app.register_blueprint(auth_bp)

db.init_app(app)

@app.route('/heartbeat')
def heartbeat():
    return jsonify({'hello': 'world'})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
    #with app.app_context():
    #    db.create_all()
