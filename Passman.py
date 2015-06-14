from hashlib import sha256

SECRET_KEY = 's3cr3t'

def get_hexdigest(text1, text2):
    return sha256(text1 + text2).hexdigest()

def make_password(plaintext, service):
    salt = get_hexdigest(SECRET_KEY, plaintext)
    hsh = get_hexdigest(salt, service)
    return ''.join(salt + hsh)

if __name__ == '__main__':
    print make_password('password', 'facebook')
