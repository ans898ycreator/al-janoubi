import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secure_key_999'
socketio = SocketIO(app, cors_allowed_origins="*")

server_data = {
    "general_candidates": [],
    "battle_scores": {"A": 0, "B": 0},
    "battle_timer_end": 0,
    "general_timer_end": 0
}

# عداد المشاهدين المتصلين حالياً
connected_users = 0

@socketio.on('connect')
def handle_connect():
    global connected_users
    connected_users += 1
    # إرسال عدد المشاهدين المحدث لكل المتواجدين
    socketio.emit('update_viewers', {'count': connected_users})
    socketio.emit('broadcast_state', server_data)

@socketio.on('disconnect')
def handle_disconnect():
    global connected_users
    connected_users = max(0, connected_users - 1)
    socketio.emit('update_viewers', {'count': connected_users})

# المسارات (Routes)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions')
def questions_page():
    return render_template('questions.html')

@app.route('/random')
def random_page():
    return render_template('games.html')

@app.route('/ruligs')
def ruligs_page():
    return render_template('ruligs.html')

@app.route('/confess')
def confess_page():
    return render_template('random.html')

@app.route('/dice')
def dice():
    return render_template('dice.html')

@app.route('/sevens')
def sevens():
    return render_template('sevens.html')

@app.route('/vote')
def vote_page():
    return render_template('vote.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

# أحداث التزامن والمزامنة للبث واللعب
@socketio.on('sync_action')
def handle_sync(data):
    global server_data
    if not data:
        return

    action = data.get('type')

    if action == 'battle_score_update':
        side = data.get('side')
        if side in server_data["battle_scores"]:
            server_data["battle_scores"][side] = data.get('score', server_data["battle_scores"][side])
            socketio.emit('broadcast_state', server_data)

    elif action == 'reset_everything':
        server_data = {
            "general_candidates": [],
            "battle_scores": {"A": 0, "B": 0},
            "battle_timer_end": 0,
            "general_timer_end": 0
        }
        socketio.emit('broadcast_state', server_data)

# تم تعديل مكانها لتكون منفصلة وصحيحة
@socketio.on('player_action')
def handle_player_action(data):
    socketio.emit('update_view', data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
