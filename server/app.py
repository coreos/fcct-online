from flask import Flask, jsonify, request
from flask_cors import CORS
import urllib.parse as parse
import os
from subprocess import Popen, PIPE, STDOUT


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
    string = 'variant: fcosversion: 1.0.0 passwd: users:    - name: core      ssh_authorized_keys:        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC6jeR8fMqwxDsoVdc62m+V6L9QWH7MSJ+zmmrE0UWClF3iuFJ5belHxXNg/6wnpefyu5hKrrwCGjcfxNxH438MYuUOBxo5CwZHI3d3+kkMudidEhFJxMhk+S9I5XnBRjhzQrTnqcf2BULW4kV6JfrLSx2TQxvaUh9d59tJa5J6sFtob6Iil/qY9oyKQQHA/+7+xgCqWW2P/lgkBCLk1+ll+F0nNCTygUJjWyRWy3lUDo5edwyV8cqoYJVmE1dcBAqV7GwflrlSf+RzAVa8S5hxpdKyXs9SVVlFoN3/SjwaJnJX/oQWPbubraBm3/7sAC2pLAo9BuSRYdylUJyS9NGhNK2ibdB4o5rWREynnX6Lr4FotzIAQg+xDFRc9EX+sHHaTOWXDebFzL4aJEPn1XA0hQ5zzK5PZyL6l1v+qiz16o4hO4PlRaW5FmNndjCJ3yREalIZBp6a9PCdNw9K4LPcPQ1ZYjxx6bn1SWXbRodKpdSQqLlzKeUNjH0Aro6+TB8= abai@unused-10-15-17-19.yyz.redhat.com'
    encoded_string = 'variant%3A%20fcosversion%3A%201.0.0%20passwd%3A%20users%3A%20%20%20%20-%20name%3A%20core%20%20%20%20%20%20ssh_authorized_keys%3A%20%20%20%20%20%20%20%20-%20ssh-rsa%20AAAAB3NzaC1yc2EAAAADAQABAAABgQC6jeR8fMqwxDsoVdc62m%2BV6L9QWH7MSJ%2BzmmrE0UWClF3iuFJ5belHxXNg%2F6wnpefyu5hKrrwCGjcfxNxH438MYuUOBxo5CwZHI3d3%2BkkMudidEhFJxMhk%2BS9I5XnBRjhzQrTnqcf2BULW4kV6JfrLSx2TQxvaUh9d59tJa5J6sFtob6Iil%2FqY9oyKQQHA%2F%2B7%2BxgCqWW2P%2FlgkBCLk1%2Bll%2BF0nNCTygUJjWyRWy3lUDo5edwyV8cqoYJVmE1dcBAqV7GwflrlSf%2BRzAVa8S5hxpdKyXs9SVVlFoN3%2FSjwaJnJX%2FoQWPbubraBm3%2F7sAC2pLAo9BuSRYdylUJyS9NGhNK2ibdB4o5rWREynnX6Lr4FotzIAQg%2BxDFRc9EX%2BsHHaTOWXDebFzL4aJEPn1XA0hQ5zzK5PZyL6l1v%2Bqiz16o4hO4PlRaW5FmNndjCJ3yREalIZBp6a9PCdNw9K4LPcPQ1ZYjxx6bn1SWXbRodKpdSQqLlzKeUNjH0Aro6%2BTB8%3D%20abai%40unused-10-15-17-19.yyz.redhat.com'
    decoded_string = parse.unquote(fcc)

    ignition_config = Popen('./fcct-x86_64-unknown-linux-gnu', stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout = ignition_config.communicate(input=fcc.encode())[0]
    return jsonify(stdout.decode())

if __name__ == '__main__':
    app.run()
