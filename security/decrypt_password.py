"""
Standalone tool for decrypting device secrets
Uses encryption.py to do the actual work

Modules:
    3rd Party: base64
    Custom: encryption

Classes:

    None

Functions

    main()
        Main function

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - May 2023
"""


import base64

import encryption


def main():
    """
    Main function

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

    # Get secret and salt from the user
    secret = input('Enter secret to decrypt: ')
    salt = input('Enter salt: ')

    with encryption.CryptoSecret() as decryptor:
        # Decrypt the password
        password = decryptor.decrypt(
            secret=secret,
            salt=base64.urlsafe_b64decode(salt.encode())
        )

    # Print the decrypted password
    print(f'Decrypted password: {password}')


if __name__ == '__main__':
    main()
