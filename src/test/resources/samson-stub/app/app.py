#!flask/bin/python
#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from flask import Flask
from flask import request
from flask import make_response
from functools import wraps
import os, io, json

app = Flask(__name__)

def getFile( fileName, status="200" ):
     filePath = "/samson-stub/responses/%s" % fileName
     if not os.path.isfile(filePath):
        raise AuthError({"code": "response_file_not_found", "description": "Unable to load response file"}, 500)

     f = io.open(filePath, "r", encoding="utf-8")

     resp = make_response( (f.read(), status) )
     resp.headers['Content-Type'] = 'application/json; charset=utf-8'

     return resp

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/projects/<project_name>/deploys/<deploy_id>.json', methods=['GET'])
def get_deploy_data(project_name, deploy_id):
    return getFile("deploy_%s.json" % deploy_id)

@app.route('/integrations/generic/<webhook_id>', methods=['POST'])
def start_deploy(webhook_id):
    return getFile("start_deploy_%s.json" % webhook_id)

@app.route('/projects/<project_name>')
def get_project(project_name):
    return "{}"

if __name__ == '__main__':
    app.run(debug=True)
