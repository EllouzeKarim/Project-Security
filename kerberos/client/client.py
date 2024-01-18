#!/usr/bin/python3
from KerberosClient import KerberosClient

krb = KerberosClient("host@kdc.insat.tn")
SERVER_URL = 'http://kdc.insat.tn:5000'
RED = "\033[31m"
RESET = "\033[0m"


def output_in_red(msg):
    print(RED + msg + RESET)


def handle_response(response):
    if response is None:
        output_in_red(
            "Something went wrong, please check your kerberos ticket!")
    elif response.status_code == 200:
        output_in_red(response.content.decode("utf-8"))
    else:
        print(
            f'Error {response.status_code}: {response.content.decode("utf-8")}')


def menu():
    """Display a menu to the user and get their choice."""
    print('1. Read a file')
    print('2. Quit')
    choice = input('Enter your choice (1/2/3/4): ')
    return choice

def read_file():
    """Read a file on the Flask server."""
    file_path = input('Enter the file path: ')
    data = {"file_path": file_path}
    response = krb.post(
        f"{SERVER_URL}/read_file", data)
    handle_response(response)





def main():
    while True:
        choice = menu()
        if choice == '1':
            read_file()
        elif choice == '2':
            break
        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()