import os
import uuid
import json
import re

from subprocess import Popen, PIPE, STDOUT
import urllib.parse as parse

from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/config/', methods=['POST'])
def fcc_to_ignition():
    post_data = request.get_json()
    response_object = {}

    # handle '/config/'
    if post_data.get('config_string') == '':
        return jsonify(response_object)

    # run fcct on the config
    ignition_config = Popen(
        './fcct-x86_64-unknown-linux-gnu',
        stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout = ignition_config.communicate(input=post_data.get('config_string').encode())[0]

    try:
        response_object = {'success': True, 'message': json.loads(stdout.decode())}
    except:
        errmsg = stdout.decode()

        # format error message
        line_no_info = re.findall(r'[ |\n]*line \d:', errmsg)
        err_lines = []
        for str in line_no_info:
            errmsg = errmsg.replace(str, '\n' + str.strip())
            err_lines.append(int(re.search(r'\d+', str).group()))

        response_object = {'success': False, 'message': errmsg, 'err_lines': err_lines}

    return jsonify(response_object)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
