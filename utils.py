import db_utils

# Функция проверки наличия ошибки при регистрации
def validate_reg(login:str, password:str, password_repeat:str, word:str) -> tuple:
    if not(login and password and password_repeat and word): 
        return (False, 'Fill in all the fields')
    elif db_utils.check_login(login):
        return (False, 'A user with this login already exists')
    else: 
        password_check(password, password_repeat)
   
# Функция проверки паролей 
def password_check(password:str, password_repeat:str) -> tuple:
    if password != password_repeat: 
        return (False, 'Password mismatch')
    elif len(password) < 4: 
        return (False, 'The password is too short')
    else:
        return (True, '')
    