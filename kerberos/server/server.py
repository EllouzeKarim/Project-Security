#!/usr/bin/env python

from flask import Flask, request
from flask_kerberos import init_kerberos
from flask_kerberos import requires_authentication
import helpers
import os

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
@requires_authentication
def index(user):
    return f"Authentication successfull, mister {user}"


@app.route('/read_file', methods=['POST'])
@requires_authentication
def read_file(principal):
    user = helpers.unix_user(principal)
    home = helpers.get_user_home_dir(user)
    # Get the file path from the request form
    file_path = request.form.get('file_path')
    if file_path:
        file_path = home + file_path
        print(file_path)
        try:
            # Open the file in text mode for reading
            with open(file_path, 'r') as file:
                # Read the file contents as text
                file_contents = file.read()
                # Return the file contents as the response
                return file_contents
        except FileNotFoundError:
            return 'File not found', 404
    else:
        return 'File path parameter is missing', 400




if __name__ == '__main__':
    init_kerberos(app, service="host")
    app.run(host='0.0.0.0')