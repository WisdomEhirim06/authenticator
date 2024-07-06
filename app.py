from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URL'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

app.register_blueprint(auth.bp)
app.register_blueprint(users.bp)
app.register_blueprint(organisations.bp)

if __name__ == '__main__':
    app.run(debug=True)
