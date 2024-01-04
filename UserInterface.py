from abc import ABC, abstractmethod
from AddressBook import *

class UserInterface(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_commands(self, commands):
        pass

    @abstractmethod
    def get_user_input(self, prompt):
        pass

    @abstractmethod
    def display_message(self, message):
        pass

class ConsoleInterface(UserInterface):
    def display_contacts(self, contacts):
        if not contacts:
            self.display_message("No contacts found.")
            return

        for contact in contacts:
            self.display_message(str(contact))
            days_to_birthday = contact.days_to_birthday() if hasattr(contact, 'days_to_birthday') else None
            if days_to_birthday is not None:
                self.display_message(f"Days to birthday: {days_to_birthday}")
            self.display_message("_" * 50)

    def display_commands(self, commands):
        self.display_message("Available commands:")
        for command in commands:
            self.display_message(command)

    def get_user_input(self, prompt):
        while True:
            user_input = input(f"{prompt}: ")
            if user_input:
                return user_input
            else:
                self.display_message("Invalid input. Please try again.")

    def display_message(self, message):
        print(message)

class Bot:
    def __init__(self, user_interface):
        self.book = AddressBook()
        self.ui = user_interface

    def handle(self, action):
        try:
            if action == 'add':
                name = Name(input("Name: ")).value.strip()
                phones = Phone().value
                birth = Birthday().value
                email = Email().value.strip()
                status = Status().value.strip()
                note = Note(input("Note: ")).value
                record = Record(name, phones, birth, email, status, note)
                return self.book.add(record)
            
            elif action == 'search':
                print("There are following categories: \nName \nPhones \nBirthday \nEmail \nStatus \nNote")
                category = input('Search category: ')
                pattern = input('Search pattern: ')
                result = (self.book.search(pattern, category))
                for account in result:
                    if account['birthday']:
                        birth = account['birthday'].strftime("%d/%m/%Y")
                        result = "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {', '.join(account['phones'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50
                        print(result)

            elif action == 'edit':
                contact_name = input('Contact name: ')
                parameter = input('Which parameter to edit(name, phones, birthday, status, email, note): ').strip()
                new_value = input("New Value: ")
                return self.book.edit(contact_name, parameter, new_value)
            
            elif action == 'remove':
                pattern = self.ui.get_user_input("Remove (contact name or phone): ")
                if self.book.remove(pattern):
                    self.ui.display_message(f"Contact with {pattern} removed successfully.")
                else:
                    self.ui.display_message(f"No contact found with {pattern}.")

            elif action == 'save':
                file_name = self.ui.get_user_input("File name: ")
                self.book.save(file_name)
                self.ui.display_message(f"Address book saved to {file_name}.")

            elif action == 'load':
                file_name = self.ui.get_user_input("File name: ")
                self.book.load(file_name)
                self.ui.display_message(f"Address book loaded from {file_name}.")

            elif action == 'congratulate':
                self.ui.display_message(self.book.congratulate())

            elif action == 'view':
                self.ui.display_contacts(self.book)

            elif action == 'exit':
                return False

            else:
                self.ui.display_message("Invalid command. Please enter a valid command.")

        except Exception as e:
            self.ui.display_message(f"Error: {str(e)}")
            
        return True

    def run(self):
        commands = ['Add', 'Search', 'Edit', 'Load', 'Remove', 'Save', 'Congratulate', 'View', 'Exit']
        while True:
            action = self.ui.get_user_input('Type help for list of commands or enter your command').strip().lower()
            if action == 'help':
                self.ui.display_commands(commands)
                action = self.ui.get_user_input('').strip().lower()

            if not self.handle(action):
                break

            if action in ['add', 'remove', 'edit']:
                self.book.save("auto_save")            

if __name__ == "__main__":
    console_ui = ConsoleInterface()
    bot = Bot(console_ui)
    bot.book.load("auto_save")
    bot.run()