import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordData:

    def __init__(self):
        self.passwords = {}
        self.fernet = None
        self.file_location = './passwords.dat'

    def verify_login(self, first_password):
        # check if password is correct
        # get hash from file
        hash_file = open('./password_hash.dat', 'r')
        _hash = hash_file.read()
        hash_file.close()
        
        if (hashlib.sha224(first_password.encode()).hexdigest() == _hash):
            print('access granted')

            # generate key and fernet
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'\xc5o\xa4\x87\x060%"\xfb\xb9\xe9\x04\xed\x95`\x1f',
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(first_password.encode()))
            self.fernet = Fernet(key)
            self.get_passwords()
            return True
        else:
            return False

    def get_passwords(self):
        # open and read file
        p_file = open(self.file_location, 'rb')
        lines = p_file.readlines()
        p_file.close()

        # check if file is emtpy if it isnt decrypt the contents and construct the password dict
        if os.path.getsize(self.file_location) > 0:
            for line in lines:
                line_str = self.fernet.decrypt(line.strip()).decode()
                info = line_str.split(',')
                self.passwords[info[0]] = {
                    'username': info[1],
                    'password': info[2]
                }
    
    def save_passwords(self):
        password_file = open(self.file_location, 'wb')
        for site in self.passwords:
            password_file.write(self.fernet.encrypt((site+','+self.passwords[site]['username']+','+self.passwords[site]['password']).encode()))
            password_file.write(b'\n')
        password_file.close()
