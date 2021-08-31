#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_get_api_token

short_description: Get API credentials for use with Rancher

version_added: "1.0"

description:
    - "This module outputs a time-limited bearer token for use with the Rancher API"

options:
    rancher_domain:
        description:
            - The URL of the Rancher UI instance to login to
        required: true
    rancher_username:
        description:
            - The Rancher username to login with
        required: true
    rancher_password:
        description:
            - The Rancher password to login with
        required: true
    ttl:
        description:
            - The desired TTL of the Rancher API credentials, in seconds
        required: false
        default: 10000

author:
    - Guy
'''

EXAMPLES = '''
- name: Register Rancher API token
  rancher_get_api_token
    rancher_domain: rancher.lab.int
    rancher_username: admin
    rancher_password: password
    ttl: 300
  register: rke_bearer_token

- name: Some other module that requires a token
  other_module:
    api_bearer_token: rke_bearer_token.token
'''

RETURN = '''
token:
    description: A bearer token for the Rancher API
    type: string
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import basic_auth_header, fetch_url, url_argument_spec
import json

class RancherGetApiToken(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            rancher_domain=dict(type='str', required=True),
            rancher_username=dict(type='str', required=True),
            rancher_password=dict(type='str', required=True),
            ttl=dict(type='int', default=10000),
        )

        # Module input variables
        self.rancher_domain = None
        self.rancher_username = None
        self.rancher_password = None
        self.ttl = None

        # Internal variables that aren't set through the module input
        self.path = '/v3-public/localProviders/local?action=login'

        self.results = dict(
            changed=False,
            token='',
        )

        self.module = AnsibleModule(
            argument_spec=self.module_spec,
            supports_check_mode=True
        )

        res = self.exec_module(**self.module.params)
        self.module.exit_json(**res)

    def exec_module(self, **kwargs):
        for key in list(self.module_spec.keys()):
            setattr(self, key, kwargs[key])

        token = self.get_token()

        if token is False:
            self.module.fail_json(msg='Unable to retrieve API token')
        else:
            self.results['token'] = token
            self.results['changed'] = True

        return self.results

    def get_token(self):
        headers = {
            "Authorization": str(basic_auth_header(self.rancher_username, self.rancher_password)),
            "Content-Type": "application/json"
        }

        data = {
            'name': 'ansible_generated',
            'username': self.rancher_username,
            'password': self.rancher_password,
            'ttl': self.ttl
        }

        request_type = 'POST'
        resp, info = fetch_url(
            self.module,
            self.rancher_domain + self.path,
            headers=headers,
            method=request_type,
            data=json.dumps(data)
        )

        if info["status"] != 201:
            reason = 'Rancher gave the status code of ' + str(info["status"]) + ' wehn trying to retrieve an API token'
            self.module.fail_json(msg='API token request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())
        try:
            token = decoded_response["token"]
            return token
        except:
            return False

def main():
    RancherGetApiToken()

if __name__ == '__main__':
    main()