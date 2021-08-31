#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: gitlab_instance_variable

short_description: This module manages an instance variable in gitlab

version_added: "1.0"

description:
    - This module manages instance variables in gitlab for a given domain.

options:
    gitlab_url:
        description:
            - The gitlab domain name, e.g. rancher.cloudranger.co.uk
        required: true
    private_token:
        description:
            - The private token used to authorise the command.
        required: true
    variable_name:
        description:
            - The name of the variable to be set on the instance.
        required: true
    variable_value:
        description:
            - The value of the variable to be set on the instance.
        required: true


author:
    - Guy
'''

EXAMPLES = '''
- name: Gitlab | Set instance Variable
  gitlab_instance_variable:
    gitlab_url: https://gitlab.example.com
    private_token: <PRIVATE TOKEN>
    variable_name: foo
    variable_value: bar
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


class GitlabInstanceVariable(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            gitlab_url=dict(type='str', required=True),
            private_token=dict(type='str', required=True, no_log=True),
            variable_name=dict(type='str', required=True),
            variable_value=dict(type='str', required=True),
        )

        # Module input variables
        self.gitlab_url = None
        self.private_token = None
        self.variable_name = None
        self.variable_value = None

        self.results = dict(
            changed=False,
        )

        self.module = AnsibleModule(
            argument_spec=self.module_spec,
            supports_check_mode=True
        )

        res = self.exec_module(**self.module.params)
        self.module.exit_json(**res)

    def get_variable(self, **kwargs):
        # Internal variables that aren't set through the module input
        path = '/api/v4/admin/ci/variables/' + self.variable_name

        headers = {
            'PRIVATE-TOKEN': self.private_token,
        }

        request_type = 'GET'

        resp, info = fetch_url(self.module, self.gitlab_url + path, headers=headers, method=request_type)

        if info["status"] == 200:
            return json.loads(resp.read())
        elif info["status"] == 404:
            return None

        reason = 'Gitlab gave a status code of ' + str(info["status"])

        self.module.fail_json(msg='Gitlab Variable get request unsuccessful. ' + reason)

    def update_variable(self, **kwargs):
        # Internal variables that aren't set through the module input
        path = '/api/v4/admin/ci/variables/' + self.variable_name

        headers = {
            'PRIVATE-TOKEN': self.private_token,
            'Content-Type': 'application/json',
        }

        request_type = 'PUT'

        data = {
            "value": self.variable_value,
        }

        resp, info = fetch_url(self.module, self.gitlab_url + path, headers=headers, data=json.dumps(data),
                               method=request_type)

        if info["status"] != 200:
            reason = 'Gitlab gave a status code of ' + str(info["status"])
            self.module.fail_json(msg='Gitlab Variable put request unsuccessful. ' + reason)

        self.results["changed"] = True

    def create_variable(self):
        # Internal variables that aren't set through the module input
        path = '/api/v4/admin/ci/variables'

        headers = {
            'PRIVATE-TOKEN': self.private_token,
            'Content-Type': 'application/json',
        }

        request_type = 'POST'

        data = {
            "key": self.variable_name,
            "value": self.variable_value,
        }

        resp, info = fetch_url(self.module, self.gitlab_url + path, headers=headers, data=json.dumps(data),
                               method=request_type)

        if info["status"] != 201:
            reason = 'Gitlab gave a status code of ' + str(info["status"])
            self.module.fail_json(msg='Gitlab Variable post request unsuccessful. ' + reason)

        self.results["changed"] = True

    def exec_module(self, **kwargs):
        for key in list(self.module_spec.keys()):
            setattr(self, key, kwargs[key])

        result = self.get_variable()

        if result is None:
            self.create_variable()
        elif result["value"] != self.variable_value:
            self.update_variable()

        return self.results


def main():
    GitlabInstanceVariable()


if __name__ == '__main__':
    main()
