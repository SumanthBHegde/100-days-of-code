from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#Generating a key from the password
def generate_key(password):
    
    # Convert to bytes
    password = password.encode()
    
    # Fixed salt for simplicity
    salt = b'\x0c\xda\x9f\x19\xb2\xf1\xf3\xe1\x15\xed\x19\xbe\xab\x8b\xe1\x95'
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )
    
    # Convert to base64 key
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

# Encrypt a file
def encrypt_file(file_path, password):
    try:
        key = generate_key(password)
        fernet = Fernet(key)
        
        with open(file_path, 'rb') as file:
            original_data = file.read()
            
        encrypted_data = fernet.encrypt(original_data)
        
        with open(file_path + ".encrypted", 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
            
        print(f"File '{file_path}' has been encrypted succesfully! ")
    except Exception as e:
        print(f"Error : {e}")
        
# Decrypt a file
def decrypt_file(encrypted_file_path, password):
    try:
        key = generate_key(password)
        fernet = Fernet(key)
        
        with open(encrypted_file_path, 'rb') as file:
            encrypted_data = file.read()
            
        decrypted_data = fernet.encrypt(encrypted_data)
        
        with open(encrypted_file_path.replace(".encrypted", ""), 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
            
        print(f"File '{encrypted_file_path}' has been decrypted succesfully! ")
    except Exception as e:
        print(f"Error : {e}")
        
# Main CLI for user interaction
def main():
    while True:
        print("\n1. Encrypt a File")
        print("2. Decrypt a File")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            file_path = input("Enter the file path to encrypt: ").strip()
            password = input("Enter the password for encryption: ").strip()
            encrypt_file(file_path, password)
        
        elif choice == "2":
            encrypted_file_path = input("Enter the encrypted file path: ").strip()
            password = input("Enter the password for decryption: ").strip()
            decrypt_file(encrypted_file_path, password)
        
        elif choice == "3":
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main() 