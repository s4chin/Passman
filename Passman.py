import argparse
import sys

from hashlib import sha256

from config import SECRET_KEY, ALPHABET, SYMBOL

from peewee import *

db = SqliteDatabase('accounts.db')

class Service(Model):
    name = CharField()
    length = IntegerField(default=16)
    symbols = BooleanField(default=True)
    alphabet = CharField(default='')

    class Meta:
        database = db

    def get_alphabet(self):
        if self.alphabet:
            return self.alphabet
        alpha = ALPHABET
        if self.symbols:
            alpha += SYMBOL
        return alpha

    def password(self, plaintext):
        return password(plaintext, self.name, self.length, self.get_alphabet())

    @classmethod
    def search(cls, q):
        return cls.select().where(cls.name ** ('%%%%s%%' %q))

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
        chars.append(alphabet[num_chars - idx - 1])
    return ''.join(chars)



def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--service', required=True, help="Name of service")
    parser.add_argument('-p', '--password', required=True, help="Master password")
    parser.add_argument('-l', '--length', type=int, default=16, help="Length of the generated password")
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args()
    db.create_table(Service, True)
    service = Service.create(name=args.service, length=args.length, symbols=True)
    print service.password(args.password)    

if __name__ == '__main__':
    parseargs()
