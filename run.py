from flask import Flask
from app.auth.login_routes import login_bp
from app.auth.signup_routes import signup_bp

app = Flask(__name__, template_folder='app/layout/templates', static_folder='app/layout/static')
app.secret_key = '3c1b41c7b50912966d49ae4a198a6a3913a76c930e9ef38e'

app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)

if __name__ == '__main__':
    app.run(debug=True)
