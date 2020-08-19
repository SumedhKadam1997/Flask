from werkzeug.security import generate_password_hash, check_password_hash

hashed = generate_password_hash('mypassword')

print(hashed)

check = check_password_hash(hashed,'mypassword')

print(check)