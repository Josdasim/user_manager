import bcrypt

def hash_password(password:str) -> str:
    salt = bcrypt.gensalt()
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hashed.decode('utf-8')

def verify_password(password:str, password_hashed:str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hashed.encode('utf-8'))