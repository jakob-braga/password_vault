# password_vault

An application that allows you to store multiple passwords in an encrypted format.

To use, run main.py, on first launch it will ask you for a password you would like to use to get into the application and then ask you to restart.
The password will be stored as a one way hash. After the first login, you can begin adding and editing passwords.
The passwords are encrypted by a fernet key that is generated from your login password, and then stored in a the passwords.dat file.
