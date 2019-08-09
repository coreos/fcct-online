#!/usr/bin/env python3
"""
Flask application code that provides a web
service for checking fcct configs.
"""

import json
import os
import re

from subprocess import Popen, PIPE, STDOUT

from flask import Flask, jsonify, request
from flask_cors import CORS

# configuration which is read by app.config.from_object
#: If the server should run in debug mode
DEBUG = os.getenv('ONLINE_FCCT_DEBUG', False)
#: The max length allowed for the posted fcct config
MAX_LENGTH = os.getenv('ONLINE_FCCT_MAX_LENGTH', 31415)

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/config/', methods=['POST'])
def fcc_to_ignition():
    """
    Handles web ui request to turn fcc to ignition.

    :returns: JSON Flask response
    :rtype: flask.Response
    """
    # make sure request content type is json
    if not request.mimetype == 'application/json':
        return jsonify('failed: Content-type must be application/json'), 401

    post_data = request.get_json()
    response_object = {}

    # check length of config_string
    if (len(post_data.get('config_string').encode()) > MAX_LENGTH):
        return jsonify('failed: FCC string too long'), 400

    # run fcct on the config
    ignition_config = Popen(
        './fcct-x86_64-unknown-linux-gnu',
        stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout = ignition_config.communicate(
        input=post_data.get('config_string').encode())[0]

    # construct response object
    try:
        response_object = {'success': True,
                           'message': json.loads(stdout.decode())}
    except (json.decoder.JSONDecodeError):
        errmsg = stdout.decode()

        # format error message
        line_no_info = re.findall(r'[ |\n]*line \d:', errmsg)
        err_lines = []
        for section in line_no_info:
            errmsg = errmsg.replace(section, '\n' + section.strip())
            err_lines.append(int(re.search(r'\d+', section).group()))

        response_object = {'success': False,
                           'message': errmsg,
                           'err_lines': err_lines}

    return jsonify(response_object)


if __name__ == '__main__':
    # If the module is called directly, run a debug server
    app.run(debug=True, port=5000)
