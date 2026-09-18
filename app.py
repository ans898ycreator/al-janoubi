from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

connected_viewers = 0
last_action = {"message": "في انتظار بدء الأحداث..."}

@app.route('/')
def host_page():
    # هذه صفحتك الخاصة كمضيف
    return render_template('host.html')

@app.route('/viewer')
def viewer_page():
    # هذا الرابط المنفصل الخاص بالمشاهدين والمتابعين
    return render_template('viewer.html')

@socketio.on('connect')
def handle_connect():
    global connected_viewers
    connected_viewers += 1
    emit('update_viewers', {'count': connected_viewers}, broadcast=True)
    # إرسال آخر حالة فور اتصال المشاهد الجديد
    emit('update_view', last_action)

@socketio.on('disconnect')
def handle_disconnect():
    global connected_viewers
    if connected_viewers > 0:
        connected_viewers -= 1
    emit('update_viewers', {'count': connected_viewers}, broadcast=True)

# استقبال الحركة من صفحة المضيف وبثها للمشاهدين حصراً
@socketio.on('host_action')
def handle_host_action(data):
    global last_action
    last_action = data
    socketio.emit('update_view', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
