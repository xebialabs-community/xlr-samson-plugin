#
# Copyright 2019 XEBIALABS
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

    def __init__(self, httpConnection, webhookToken, maxChecksPerDeploymentId=30, timeout=5):
        self.httpConnection = httpConnection
        self.httpRequest = HttpRequest(httpConnection)
        self.webhookToken = webhookToken
        self.headers = self._get_headers()
        self.maxChecksPerDeploymentId = maxChecksPerDeploymentId
        self.timeout = timeout

    @staticmethod
    def create_client(httpConnection, webhookToken):
        return SamsonClient(httpConnection, webhookToken)

    def _get_headers(self):
        return {"Accept": "application/json", "Content-Type": "application/json",
                "Authorization": "Bearer %s" % self.webhookToken}

    def ping(self, project_name):
        # random valid endpoint that verifies we're logged in / have a valid token
        url = '/projects/%s' % project_name
        response = self.httpRequest.get(url, headers=self.headers)
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            print json.dumps(data)
        else:
            self.throw_error(response)

    def start_deploy(self, webhook_id, commit_sha, message, branch="master"):
        url = "/integrations/generic/%s" % webhook_id
        body = {
            "deploy": {
                "branch": branch,
                "commit": {
                    "sha": commit_sha,
                    "message": message
                }
            }
        }

        print "body = %s" % json.dumps(body)

        # example response: {"deploy_ids":[],"messages":"INFO: Branch master is release branch: true\nINFO: Deploying to 0 stages\n"}
        response = self.httpRequest.post(url, headers=self.headers, body=json.dumps(body))

        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            print json.dumps(data["deploy_ids"])
            print json.dumps(data["messages"])
            return data
        else:
            self.throw_error(response)

    def wait_for_deploy(self, project_name, deploy_id):
        # /projects/gcr-watcher/deploys/44.json
        url = "/projects/%s/deploys/%s.json" % (project_name, deploy_id)
        status = ""
        number_of_checks = 0

        while status not in ["succeeded", "failed"]:
            response = self.httpRequest.get(url, headers=self.headers)

            if response.getStatus() in HTTP_SUCCESS:
                depData = json.loads(response.getResponse())["deploy"]
                status = depData["status"]
                depReportUrl = depData["url"]            

                number_of_checks += 1
                if number_of_checks > self.maxChecksPerDeploymentId:
                    sys.exit("Fail: project %s deployment %s failed" % (project_name, deploy_id))

                time.sleep(self.timeout)
            else:
                self.throw_error(response)

            if status == "failed":
                sys.exit("Fail: project %s deployment %s failed" % (project_name, deploy_id))
            else:
                print "Success: project %s deployment %s succeeded" % (project_name, deploy_id)

    def throw_error(self, response):
        msg = "Error from server, HTTP Return: %s, content %s\n" % (response.getStatus(), response.getResponse())
        print msg
        sys.exit(msg)
