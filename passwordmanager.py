"""
Enhanced Password Manager

A secure password manager with encryption, password generation,
search functionality, and improved user interface.
"""

import os
import json
import base64
import secrets
import string
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PasswordManager:
    """Enhanced password manager with advanced features."""
    
    def __init__(self, master_password: str = None):
        self.key_file = "key.key"
        self.passwords_file = "passwords.json"
        self.master_password = master_password
        self.fernet = None
        self.passwords = {}
        
        self.initialize_encryption()
        self.load_passwords()
    
    def initialize_encryption(self):
        """Initialize encryption with master password."""
        if not os.path.exists(self.key_file):
            if not self.master_password:
                self.master_password = self.get_master_password()
            
            # Generate key from master password
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.master_password.encode()))
            
            # Save salt and key
            with open(self.key_file, "wb") as key_file:
                key_file.write(salt + b"|" + key)
        else:
            # Load existing key
            with open(self.key_file, "rb") as key_file:
                data = key_file.read()
                salt, key = data.split(b"|", 1)
                
                if self.master_password:
                    # Verify master password
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=100000,
                    )
                    try:
                        kdf.verify(self.master_password.encode(), base64.urlsafe_b64decode(key))
                    except:
                        raise ValueError("Incorrect master password!")
                else:
                    self.master_password = self.get_master_password()
                    # Verify master password
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=100000,
                    )
                    try:
                        kdf.verify(self.master_password.encode(), base64.urlsafe_b64decode(key))
                    except:
                        raise ValueError("Incorrect master password!")
        
        self.fernet = Fernet(key)
    
    def get_master_password(self) -> str:
        """Get master password from user."""
        print("🔐 SETUP MASTER PASSWORD")
        print("=" * 30)
        print("Create a strong master password to encrypt your passwords.")
        print("This password will be required to access your passwords.")
        print("=" * 30)
        
        while True:
            password = input("Enter master password: ").strip()
            if len(password) < 8:
                print("❌ Password must be at least 8 characters long.")
                continue
            
            confirm = input("Confirm master password: ").strip()
            if password == confirm:
                return password
            else:
                print("❌ Passwords don't match. Try again.")
    
    def generate_password(self, length: int = 16, include_symbols: bool = True) -> str:
        """Generate a secure random password."""
        characters = string.ascii_letters + string.digits
        if include_symbols:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        while True:
            password = ''.join(secrets.choice(characters) for _ in range(length))
            # Ensure password has at least one of each required character type
            if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password) and
                (not include_symbols or any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password))):
                return password
    
    def add_password(self, account: str, username: str, password: str = None, notes: str = ""):
        """Add a new password entry."""
        if not password:
            print("\n🔧 PASSWORD GENERATION")
            print("=" * 25)
            try:
                length = int(input("Password length (8-50): ") or "16")
                length = max(8, min(50, length))
                
                include_symbols = input("Include symbols? (y/n): ").lower().startswith('y')
                password = self.generate_password(length, include_symbols)
                print(f"Generated password: {password}")
            except ValueError:
                password = self.generate_password()
                print(f"Generated password: {password}")
        
        # Encrypt sensitive data
        encrypted_username = self.fernet.encrypt(username.encode()).decode()
        encrypted_password = self.fernet.encrypt(password.encode()).decode()
        encrypted_notes = self.fernet.encrypt(notes.encode()).decode()
        
        self.passwords[account] = {
            'username': encrypted_username,
            'password': encrypted_password,
            'notes': encrypted_notes,
            'created': self.get_timestamp()
        }
        
        self.save_passwords()
        print(f"✅ Password for '{account}' added successfully!")
    
    def view_passwords(self, search_term: str = None):
        """View all passwords or search for specific ones."""
        if not self.passwords:
            print("📭 No passwords stored yet.")
            return
        
        print("\n🔍 STORED PASSWORDS")
        print("=" * 60)
        
        filtered_passwords = self.passwords
        if search_term:
            filtered_passwords = {
                account: data for account, data in self.passwords.items()
                if search_term.lower() in account.lower()
            }
        
        if not filtered_passwords:
            print(f"No passwords found matching '{search_term}'")
            return
        
        for i, (account, data) in enumerate(filtered_passwords.items(), 1):
            try:
                username = self.fernet.decrypt(data['username'].encode()).decode()
                password = self.fernet.decrypt(data['password'].encode()).decode()
                notes = self.fernet.decrypt(data['notes'].encode()).decode()
                
                print(f"\n{i}. Account: {account}")
                print(f"   Username: {username}")
                print(f"   Password: {'*' * len(password)} (use 'show {i}' to reveal)")
                if notes:
                    print(f"   Notes: {notes}")
                print(f"   Created: {data['created']}")
                print("-" * 40)
                
            except Exception as e:
                print(f"❌ Error decrypting password for '{account}': {e}")
    
    def show_password(self, index: int):
        """Show a specific password."""
        try:
            account = list(self.passwords.keys())[index - 1]
            data = self.passwords[account]
            
            username = self.fernet.decrypt(data['username'].encode()).decode()
            password = self.fernet.decrypt(data['password'].encode()).decode()
            notes = self.fernet.decrypt(data['notes'].encode()).decode()
            
            print(f"\n🔓 PASSWORD DETAILS")
            print("=" * 30)
            print(f"Account: {account}")
            print(f"Username: {username}")
            print(f"Password: {password}")
            if notes:
                print(f"Notes: {notes}")
            print(f"Created: {data['created']}")
            
        except (IndexError, KeyError):
            print("❌ Invalid password index.")
        except Exception as e:
            print(f"❌ Error decrypting password: {e}")
    
    def update_password(self, account: str):
        """Update an existing password entry."""
        if account not in self.passwords:
            print(f"❌ Account '{account}' not found.")
            return
        
        print(f"\n✏️  UPDATE PASSWORD FOR '{account}'")
        print("=" * 40)
        
        try:
            username = input("New username (press Enter to keep current): ").strip()
            if not username:
                username = self.fernet.decrypt(self.passwords[account]['username'].encode()).decode()
            
            password = input("New password (press Enter to generate): ").strip()
            if not password:
                password = self.generate_password()
                print(f"Generated password: {password}")
            
            notes = input("Notes (press Enter to keep current): ").strip()
            if not notes:
                notes = self.fernet.decrypt(self.passwords[account]['notes'].encode()).decode()
            
            # Encrypt and update
            encrypted_username = self.fernet.encrypt(username.encode()).decode()
            encrypted_password = self.fernet.encrypt(password.encode()).decode()
            encrypted_notes = self.fernet.encrypt(notes.encode()).decode()
            
            self.passwords[account] = {
                'username': encrypted_username,
                'password': encrypted_password,
                'notes': encrypted_notes,
                'created': self.passwords[account]['created'],
                'updated': self.get_timestamp()
            }
            
            self.save_passwords()
            print(f"✅ Password for '{account}' updated successfully!")
            
        except Exception as e:
            print(f"❌ Error updating password: {e}")
    
    def delete_password(self, account: str):
        """Delete a password entry."""
        if account not in self.passwords:
            print(f"❌ Account '{account}' not found.")
            return
        
        confirm = input(f"Are you sure you want to delete '{account}'? (y/n): ").lower()
        if confirm.startswith('y'):
            del self.passwords[account]
            self.save_passwords()
            print(f"✅ Password for '{account}' deleted successfully!")
        else:
            print("❌ Deletion cancelled.")
    
    def export_passwords(self, filename: str = "passwords_export.txt"):
        """Export passwords to a text file (encrypted)."""
        try:
            with open(filename, 'w') as f:
                f.write("PASSWORD MANAGER EXPORT\n")
                f.write("=" * 30 + "\n\n")
                
                for account, data in self.passwords.items():
                    try:
                        username = self.fernet.decrypt(data['username'].encode()).decode()
                        password = self.fernet.decrypt(data['password'].encode()).decode()
                        notes = self.fernet.decrypt(data['notes'].encode()).decode()
                        
                        f.write(f"Account: {account}\n")
                        f.write(f"Username: {username}\n")
                        f.write(f"Password: {password}\n")
                        if notes:
                            f.write(f"Notes: {notes}\n")
                        f.write(f"Created: {data['created']}\n")
                        f.write("-" * 30 + "\n\n")
                        
                    except Exception as e:
                        f.write(f"Account: {account} (Error decrypting)\n")
                        f.write("-" * 30 + "\n\n")
            
            print(f"✅ Passwords exported to '{filename}'")
            
        except Exception as e:
            print(f"❌ Error exporting passwords: {e}")
    
    def get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def load_passwords(self):
        """Load passwords from file."""
        if os.path.exists(self.passwords_file):
            try:
                with open(self.passwords_file, 'r') as f:
                    self.passwords = json.load(f)
            except Exception as e:
                print(f"❌ Error loading passwords: {e}")
                self.passwords = {}
    
    def save_passwords(self):
        """Save passwords to file."""
        try:
            with open(self.passwords_file, 'w') as f:
                json.dump(self.passwords, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving passwords: {e}")
    
    def show_stats(self):
        """Show password manager statistics."""
        print("\n📊 PASSWORD MANAGER STATISTICS")
        print("=" * 35)
        print(f"Total passwords: {len(self.passwords)}")
        
        if self.passwords:
            # Calculate average password length
            total_length = 0
            for data in self.passwords.values():
                try:
                    password = self.fernet.decrypt(data['password'].encode()).decode()
                    total_length += len(password)
                except:
                    pass
            
            avg_length = total_length / len(self.passwords) if self.passwords else 0
            print(f"Average password length: {avg_length:.1f} characters")
        
        print(f"Storage file: {self.passwords_file}")
        print(f"Key file: {self.key_file}")
    
    def run(self):
        """Main application loop."""
        print("🔐 ENHANCED PASSWORD MANAGER")
        print("=" * 30)
        
        while True:
            print(f"\n📋 OPTIONS:")
            print("1. Add new password")
            print("2. View all passwords")
            print("3. Search passwords")
            print("4. Show specific password")
            print("5. Update password")
            print("6. Delete password")
            print("7. Export passwords")
            print("8. Show statistics")
            print("9. Exit")
            
            try:
                choice = input("\nEnter your choice (1-9): ").strip()
                
                if choice == '1':
                    account = input("Account name: ").strip()
                    if account:
                        username = input("Username: ").strip()
                        password = input("Password (press Enter to generate): ").strip() or None
                        notes = input("Notes (optional): ").strip()
                        self.add_password(account, username, password, notes)
                    else:
                        print("❌ Account name cannot be empty.")
                
                elif choice == '2':
                    self.view_passwords()
                
                elif choice == '3':
                    search_term = input("Search term: ").strip()
                    self.view_passwords(search_term)
                
                elif choice == '4':
                    try:
                        index = int(input("Enter password number: "))
                        self.show_password(index)
                    except ValueError:
                        print("❌ Please enter a valid number.")
                
                elif choice == '5':
                    account = input("Account name to update: ").strip()
                    if account:
                        self.update_password(account)
                    else:
                        print("❌ Account name cannot be empty.")
                
                elif choice == '6':
                    account = input("Account name to delete: ").strip()
                    if account:
                        self.delete_password(account)
                    else:
                        print("❌ Account name cannot be empty.")
                
                elif choice == '7':
                    filename = input("Export filename (default: passwords_export.txt): ").strip()
                    if not filename:
                        filename = "passwords_export.txt"
                    self.export_passwords(filename)
                
                elif choice == '8':
                    self.show_stats()
                
                elif choice == '9':
                    print("👋 Thanks for using the Password Manager!")
                    break
                
                else:
                    print("❌ Invalid choice. Please enter a number between 1 and 9.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Password Manager interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")


def main():
    """Main function to start the password manager."""
    try:
        manager = PasswordManager()
        manager.run()
    except Exception as e:
        print(f"❌ Failed to start Password Manager: {e}")


if __name__ == "__main__":
    main()