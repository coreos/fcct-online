import os
import uuid

from subprocess import Popen, PIPE, STDOUT
import urllib.parse as parse

from flask import Flask, jsonify
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def index():
    return jsonify('index')


# Since we used path: here, the fcc cannot contain \n
@app.route('/config/<path:fcc>', methods=['GET', 'POST'])
def fcc_to_ignition(fcc):
    decoded_string = parse.unquote(fcc).replace("\\n", "\n")
    response_object = {}

    # create tmp file to store config
    tmp_file_name = uuid.uuid4().hex
    tmp_file = open("tmp/{}".format(tmp_file_name), "w")
    tmp_file.write(decoded_string)
    tmp_file.close()

    # run fcct on the config
    with open("tmp/{}".format(tmp_file_name), "r") as tmp:
        config = tmp.read()
        ignition_config = Popen(
            './fcct-x86_64-unknown-linux-gnu',
            stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        stdout = ignition_config.communicate(input=config.encode())[0]
        tmp.close()

    # clean up
    os.remove("tmp/{}".format(tmp_file_name))
    response_object['ignition_config'] = stdout.decode()
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
