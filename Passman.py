from hashlib import sha256

SECRET_KEY = 's3cr3t'

ALPHABET = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    'abcdefghijklmnopqrstuvwxyz'
    '0123456789!@#$%^&*()-_')

def get_hexdigest(text1, text2):
    return sha256(text1 + text2).hexdigest()

def make_password(plaintext, service):
    salt = get_hexdigest(SECRET_KEY, plaintext)
    hsh = get_hexdigest(salt, service)
    return ''.join(salt + hsh)

def password(plaintext, service, length=16, alphabet=ALPHABET):
    word = make_password(plaintext, service)

    num = int(word, 16)

    num_chars = len(alphabet)

    chars = []

    while(len(chars)<length):
        num, idx = divmod(num, num_chars)
        chars.append(alphabet[num_chars-idx])

    return ''.join(chars)

if __name__ == '__main__':
    print password('password', 'facebook')
