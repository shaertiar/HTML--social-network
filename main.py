from flask import Flask, render_template, redirect, request, session
import utils
import db_utils
import math

# Приложение
app = Flask(__name__)
app.config['SECRET_KEY'] = 'for i in range(999):'

# Функция проверки входа
def check_auth() -> bool:
    if 'auth id' in session:
        if session['auth id']: return True

    else: session['auth id'] = None

    return False

# Функция проверки наличия доступа
def has_access(for_authed=True) -> bool:
    var = for_authed and check_auth()
    return var or not var

# Основной путь
@app.route('/')
def main():
    if check_auth():
        return redirect('/user')
    return redirect('/login')

# Путь к странице авторизации
@app.route('/login')
def login():
    if has_access(False):
        return render_template('login.html')
    return redirect('/')

# Путь к старнице пользователя
@app.route('/user')
def user():
    if has_access(True):
        page = request.args.get('page', 1, type=int)
        return render_template(
            'user.html', 
            login = db_utils.get_login(session['auth id']), 
            posts = db_utils.get_posts(page),
            pages = math.ceil(db_utils.count_posts() / 5)
        )
    return redirect('/')

# Путь к попытке авторизации
@app.route('/try_login', methods=['POST'])
def try_login():
    # Получение логина и пароля
    login = request.form['login']
    password = request.form['password']

    # Проверка данных входа
    auth_result = db_utils.check_user(login, password)
    if auth_result:
        session['auth id'] = auth_result[0]
        return redirect('/user')
    else:
        return redirect('/login')

# Путь к попытке регистрации
@app.route('/reg')
def reg():
    if has_access(False):
        return render_template('register.html', error=request.args.get('error'))
    return redirect('/')

# Путь к попытке регистрации
@app.route('/try_reg', methods=['POST'])
def try_reg():
    # Получение логина и пароля
    login = request.form['login']
    password = request.form['password']
    password_repeat = request.form['password-repeat']
    word = request.form['word']

    # Проверка данных
    validation = utils.validate_reg(login, password, password_repeat, word)

    if validation[0]:
        db_utils.add_user(login, password, word)
        return redirect('/login')
    else:
        return redirect(f'/reg?error={validation[1]}')

# Вызод из аккаунта
@app.route('/logout')
def logout():
    session['auth id'] = None
    return redirect('/')

# Путь к отправлке нового поста
@app.route('/send_post', methods=['POST'])
def send_post():
    user_id = session['auth id']
    text = request.form['post-text']
    
    if text:
        db_utils.add_post(user_id, text)

    return redirect('/user')

# Путь к восстановлению пароля
@app.route('/restore_password_link')
def restore_password():
    return render_template('password restore.html')

# Попытка восстановления пароля
@app.route('/try_restore_password', methods=['POST'])
def try_restore_password():
    login = request.form['login']
    word = request.form['word']
    
    if db_utils.check_user(login, word=word):
        session['user_login_to_restore_password'] = login
        print(session['user_login_to_restore_password'])
        return redirect('/restoring_password')
    
    return render_template('password restore.html')

# Восстановление пароля
@app.route('/restoring_password')
def restoring_password():
    return render_template('restoring password.html', error=request.args.get('error'))

# Попытка восстановления пароля
@app.route('/try_restoring_password', methods=['POST'])
def try_restoring_password():
    new_password = request.form['password']
    new_password_repeat = request.form['password-repeat']
    
    # Проверка данных
    validation = utils.password_check(new_password, new_password_repeat)
    
    if validation[0]:
        db_utils.update_password(session['user_login_to_restore_password'], new_password)
        return redirect('login')
    else:
        return redirect(f'/restoring_password?error={validation[1]}')

# Запуск
app.run()