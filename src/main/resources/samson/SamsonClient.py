#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sets, sys, time, __builtin__
from urllib import urlencode
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest

HTTP_SUCCESS = sets.Set([200, 201])

class SamsonClient(object):
    
    def __init__(self, httpConnection, webhookToken):
        self.httpConnection = httpConnection
        self.httpRequest = HttpRequest(httpConnection)
        self.webhookToken = webhookToken
        self.headers = self._get_headers()
        
    @staticmethod
    def create_client(httpConnection, webhookToken):
        return SamsonClient(httpConnection, webhookToken)

    def _get_headers(self):
        return {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer %s" % self.webhookToken}

    def ping(self):
        # random valid endpoint that verifies we're logged in / have a valid token
        url = '/projects'
        response = self.httpRequest.get(url, headers=self.headers)
        if response.getStatus() in HTTP_SUCCESS: 
            data = json.loads(response.getResponse())
            print json.dumps(data)
        else:
            self.throw_error(response)

    def start_deploy(self, webhook_id, commit_sha, message):
        url = "/integrations/generic/%s" % webhook_id
        body = {
            "deploy": { 
                "branch": "master",
                "commit": {
                    "sha" : commit_sha,
                    "message" : message
                }
            }
        }

        print "body = %s" % body

        # example response: {"deploy_ids":[],"messages":"INFO: Branch master is release branch: true\nINFO: Deploying to 0 stages\n"}
        # /projects/gcr-watcher/deploys/44
        response = self.httpRequest.post(url, headers=self.headers, body=json.dumps(body))

        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            print json.dumps(data["messages"])
            return data

        self.throw_error(response)
       
    def throw_error(self, response):
        msg = "Error from server, HTTP Return: %s, content %s\n" % (response.getStatus(),  response.getResponse())
        print msg
        sys.exit(msg)
