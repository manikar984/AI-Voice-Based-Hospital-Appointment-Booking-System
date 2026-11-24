from datetime import timedelta

# Change this to a long random string before deploying
SECRET_KEY = "change-this-to-a-long-random-secret-key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

ACCESS_TOKEN_EXPIRE = timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
)