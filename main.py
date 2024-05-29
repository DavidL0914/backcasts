import threading
from flask import render_template, request, jsonify
from flask.cli import AppGroup
from __init__ import app, db, cors
from api.user import user_api
from api.player import player_api
from model.users import initUsers
from model.players import initPlayers
from api.diabetes import predict_api

db.init_app(app)

app.register_blueprint(user_api)
app.register_blueprint(player_api)
app.register_blueprint(predict_api)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/table/')
def table():
    return render_template("table.html")

@app.route('/settings/')
def settings():
    return render_template("settings.html")

@app.route('/api/users/save_settings', methods=['POST'])
def save_settings():
    try:
        settings = request.json.get('settings')

        # Update the user's settings in the database
        # (replace 'current_user' with your actual user object)
        # Example: current_user.update_settings(settings)
        # Make sure to implement this method in your User model

        return jsonify({'message': 'Settings saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.before_request
def before_request():
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://127.0.0.1:4100', 'https://davidl0914.github.io']:
        cors._origins = allowed_origin
custom_cli = AppGroup('custom', help='Custom commands')

@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()

app.cli.add_command(custom_cli)

def activate_job():
    initUsers()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8008")
