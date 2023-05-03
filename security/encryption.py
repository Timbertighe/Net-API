"""
Provides encryption and decryption for device secrets
Uses the master password stored in an environment variable (api_master_pw)

Modules:
    3rd Party: cryptography, base64, termcolor, os
    Custom: None

Classes:

    CryptoSecret
        Provides encryption and decryption for device secrets

Functions

    None

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - May 2023
"""


from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import termcolor
import os
import traceback as tb


class CryptoSecret:
    """
    Provides encryption and decryption for device secrets

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    TBA

    Methods
    -------
    decrypt(secret, salt)
        Decrypt a secret using AES256 encryption
    encrypt(password)
        Encrypt a password using AES256 encryption
    """

    def __init__(self):
        """
        Class constructor

        Gets the master password from an environment variable

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        None
        """

        # Get master PW from env variable
        self.master = os.getenv('api_master_pw')

    def __enter__(self):
        """
        Called when the 'with' statement is used

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        self
            The instantiated object
        """

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Called when the 'with' statement is finished

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        self
            None
        """

        # handle errors that were raised
        if exc_type:
            print(
                f"Exception of type {exc_type.__name__} occurred: {exc_value}"
            )
            if exc_traceback:
                print("Traceback:")
                print(tb.format_tb(exc_traceback))

    def decrypt(self, secret, salt):
        '''
        Uses a salt and the master password to decrypt the secret (password)
        The master password is stored in an environment variable

        Parameters:
            secret : str
                The secret (encrypted password)
            salt : str
                The salt used to encrypt the password

        Raises:
            None

        Returns:
            password : str
                The decrypted password
            False : boolean
                If there was a problem decrypting the password
        '''

        fernet = self.build_key(salt)

        # decrypt the encrypted message using the same key
        try:
            password = fernet.decrypt(
                secret.encode()
            ).decode('utf-8')

        except Exception as err:
            print(termcolor.colored(
                "Unable to decrypt the password",
                "red"
            ))
            print(err)
            return False

        # Return decrypted password
        return password

    def encrypt(self, password):
        '''
        Encrypts a password using AES256 encryption

        Parameters:
            password : str
                The password to encrypt
            master : str
                The master password used to encrypt the password

        Raises:
            None

        Returns:
            encrypted_message : str
                The encrypted password
            salt : str
                The salt used to encrypt the password
        '''

        # Define a salt and generate a key
        salt = os.urandom(16)
        fernet = self.build_key(salt)

        # encrypt the plaintext using AES256 encryption
        encrypted_message = fernet.encrypt(password.encode())

        return encrypted_message, salt

    def build_key(self, salt):
        '''
        Builds a key using the master password and a salt

        Parameters:
            salt : str
                The salt used to encrypt the password

        Raises:
            None

        Returns:
            fernet : Fernet
                The Fernet object used to encrypt/decrypt the password
        '''

        # generate a key using PBKDF2HMAC
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master.encode()))

        # create a Fernet object using the key
        fernet = Fernet(key)

        return fernet
