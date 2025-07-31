from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password hashing function.
def hash(password: str):
    return pwd_context.hash(password)

# Verify that a given password matches a hashed one.
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)