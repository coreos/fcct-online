import os
import uuid

from subprocess import Popen, PIPE, STDOUT
import urllib.parse as parse

from flask import Flask, jsonify, redirect, url_for, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Since we used path: here, the URL encoding cannot contain \n
# So use \\n instead and substitute to \n during parsing
@app.route('/', defaults={'fcc': ''})
@app.route('/config/', methods=['GET','POST'])
def fcc_to_ignition(fcc=''):
    if (request.method == 'POST'):
        post_data = request.get_json()
        response_object = {}

        # handle '/config/'
        if post_data == '':
            return jsonify(response_object)

        # run fcct on the config
        ignition_config = Popen(
            './fcct-x86_64-unknown-linux-gnu',
            stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        stdout = ignition_config.communicate(input=post_data.get('config_string').encode())[0]

        response_object['ignition_config'] = stdout.decode()
        return jsonify(response_object)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
