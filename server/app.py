from flask import Flask, jsonify, request
from flask_cors import CORS
from subprocess import Popen, PIPE, STDOUT
import urllib.parse as parse
import os
import uuid


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
@app.route('/config/<path:fcc>', methods=['GET','POST'])
def fcc_to_ignition(fcc):
    # test data
    encoded_string = 'variant%3A%20fcos%5C%6Eversion%3A%201.0.0%5C%6Epasswd%3A%5C%6E%20%20users%3A%5C%6E%20%20%20%20-%20name%3A%20core%5C%6E%20%20%20%20%20%20ssh_authorized_keys%3A%5C%6E%20%20%20%20%20%20%20%20-%20ssh-rsa%20AAAAB3NzaC1yc2EAAAADAQABAAABgQC6jeR8fMqwxDsoVdc62m%2BV6L9QWH7MSJ%2BzmmrE0UWClF3iuFJ5belHxXNg%2F6wnpefyu5hKrrwCGjcfxNxH438MYuUOBxo5CwZHI3d3%2BkkMudidEhFJxMhk%2BS9I5XnBRjhzQrTnqcf2BULW4kV6JfrLSx2TQxvaUh9d59tJa5J6sFtob6Iil%2FqY9oyKQQHA%2F%2B7%2BxgCqWW2P%2FlgkBCLk1%2Bll%2BF0nNCTygUJjWyRWy3lUDo5edwyV8cqoYJVmE1dcBAqV7GwflrlSf%2BRzAVa8S5hxpdKyXs9SVVlFoN3%2FSjwaJnJX%2FoQWPbubraBm3%2F7sAC2pLAo9BuSRYdylUJyS9NGhNK2ibdB4o5rWREynnX6Lr4FotzIAQg%2BxDFRc9EX%2BsHHaTOWXDebFzL4aJEPn1XA0hQ5zzK5PZyL6l1v%2Bqiz16o4hO4PlRaW5FmNndjCJ3yREalIZBp6a9PCdNw9K4LPcPQ1ZYjxx6bn1SWXbRodKpdSQqLlzKeUNjH0Aro6%2BTB8%3D%20abai%40unused-10-15-17-19.yyz.redhat.com'
    decoded_string = parse.unquote(fcc).replace("\\n", "\n")

    # create tmp file to store config
    tmp_file_name = uuid.uuid4().hex
    tmp_file = open( "tmp/{}".format(tmp_file_name), "w")
    tmp_file.write(decoded_string)
    tmp_file.close()

    # run fcct on the config
    with open("tmp/{}".format(tmp_file_name), "r") as tmp:
        config = tmp.read()
        ignition_config = Popen('./fcct-x86_64-unknown-linux-gnu', stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        stdout = ignition_config.communicate(input=config.encode())[0]
        tmp.close()

    # clean up
    os.remove("tmp/{}".format(tmp_file_name))
    return jsonify(stdout.decode())

if __name__ == '__main__':
    app.run()
