# Net-API
A network API front end, to manage distributed devices and services

Still in development, see changelog in the Wiki for status

## Configuration
    Completed in conifg.yaml
    See the wiki for details on how to use it
    
    
## API Authentication
    The API uses basic authentication.
    Each API call must have a base64 token in the Authorization header
    The token is generated in this format:
        username:password
    
    The user's password is checked via LDAP. 
    Add the user's UPN to the config file.
    
    
## Device Authentication
    Device passwords are stored in the device database. They are retrieved and decrypted using the master password.
    The master password is stored in the 'api_master_pw' environment variable.
    Passwords should be encrypted to secrets before they are added to the device database.

