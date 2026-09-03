from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# 1. صفحة تسجيل الدخول
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('login.html')

# 2. الواجهة الرئيسية
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# 3. الحقل الأول: الأسئلة العامة والمسابقات
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    return render_template('questions.html')

# 4. الحقل الثاني: ألعاب التركيز والالغاز
@app.route('/games', methods=['GET', 'POST'])
def games():
    return render_template('focus.html')

# 5. قسم الأحكام والتحديات
@app.route('/rulings', methods=['GET', 'POST'])
def rulings():
    return render_template('ruligs.html')

# 6. قسم كرسي الاعتراف
@app.route('/random', methods=['GET', 'POST'])
def random_section():
    return render_template('ask.html')

# 7. لعبة نرد الحظ
@app.route('/dice', methods=['GET', 'POST'])
def dice_game():
    return render_template('dice.html')

# 8. لعبة السبعات 77
@app.route('/sevens', methods=['GET', 'POST'])
def sevens_game():
    return render_template('sevens.html')

# 9. لوحة التحكم الخاصة بالمالك والمشرفين
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

# --- نظام مزامنة الحركات الفورية أونلاين ---
@socketio.on('player_action')
def handle_player_action(data):
    emit('update_game_state', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)