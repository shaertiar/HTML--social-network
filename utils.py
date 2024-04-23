import db_utils

def validate_reg(login:str, password:str, password_repeat:str) -> tuple:
    if not(login and password and password_repeat): 
        return (False, 'Fill in all the fields')
    elif password != password_repeat: 
        return (False, 'Password mismatch')
    elif len(password) < 4: 
        return (False, 'The password is too short')
    elif db_utils.check_login(login):
        return (False, 'A user with this login already exists')
    else: 
        return (True, '')