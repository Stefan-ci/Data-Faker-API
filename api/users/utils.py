from typing import Optional
import os, binascii, hashlib
from utils.base import BaseDataGenerator, SexChoices, Constants


class PasswordManager:
    def __init__(self, salt: Optional[bytes], iterations=100_000, dklen=32):
        """
        Password manager. Used to verify/hash a password
        
        Args:
            salt (Optional[bytes]): Salt used to encrypt/decrypt the password. Defaults to os.urandom(16).
            iterations (int, optional): Number of iterations to use while computing the password. Defaults to 100_000.
            dklen (int, optional): _description_. Defaults to 32.
        """
        
        self.encoder = "utf-8"
        self.iterations = iterations
        self.dklen = dklen
        self.salt = salt if isinstance(salt, bytes) else os.urandom(16) # salt used to cook the SAUCE ;)
    
    def get_hash_key(self, password: str):
        return hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode(self.encoder),
            salt=self.salt,
            iterations=self.iterations,
            dklen=32
        )
    
    def hash_password(self, password: str):
        return binascii.hexlify(data=self.salt + self.get_hash_key(password=password)).decode(self.encoder)
    
    def verify_password(self, stored_password, password):
        stored_bytes = binascii.unhexlify(stored_password)
        salt = stored_bytes[:16]
        old_key = stored_bytes[16:]
        
        temp_manager = PasswordManager(salt=salt)
        new_key = temp_manager.get_hash_key(password)
        
        return old_key == new_key



class UserGenerator(BaseDataGenerator):
    pass_manager = PasswordManager(salt=None)
    
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        data = []
        for i in range(1, n + 1):
            username = self.fake.user_name()
            
            data.append({
                "id": i,
                "uuid": self.fake.uuid4(),
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "email": self.fake.email(),
                "username": username,
                "phone_number": self.fake.phone_number(),
                "birth_date": self.fake.date_of_birth(minimum_age=0, maximum_age=90).isoformat(),
                "sex": self.fake.random_element([sex.value for sex in SexChoices]),
                "address": self.fake.address(),
                "postal_code": self.fake.postalcode(),
                "city": self.fake.city(),
                "country": self.fake.country(),
                "date_joined": self.fake.date_time().isoformat(),
                "last_login": self.fake.date_time().isoformat(),
                "is_active": self.fake.boolean(),
                "is_staff": self.fake.boolean(),
                "is_superuser": self.fake.boolean(),
                "password": self.pass_manager.hash_password(password=username)
            })
        return data


def generate_users_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return UserGenerator().generate(n=length)
