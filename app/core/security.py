from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hash: str):
    return pwd_context.verify(password, hash)
