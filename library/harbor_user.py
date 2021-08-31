#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: harbor_user

short_description: This module handles managing harbor users

version_added: "1.0"

description:
    - "This module creates and deletes harbor users."

options:
    harbor_domain:
        description:
            - The Name of the harbor domain
        required: true
    username:
        description:
            - The username for the user.
        required: true
    password:
        description:
            - The password for the user. Required if state is present. 
        required: false
    email:
        description:
            - The email. Required if state is present. 
        required: false
    real_name:
        description:
            - The name of the user. Required if state is present.
        required: false
    state:
        description:
            - Should the username be present or absent?
        required: true

author:
    - Guy
'''

EXAMPLES = '''
- name: Create user
  harbor_user:
    harbor_domain: harbor.example.com
    username: fred
    password: Passw0rd!
    email: test@example.com
    real_name: Fred Bloggs
    url_username: admin
    url_password: MyVery$ecureAdminPassw0rd!

- name: Delete user
  harbor_user:
    harbor_domain: harbor.example.com
    username: fred
    state: absent
    url_username: admin
    url_password: MyVerySecureAdminPassw0rd!
'''

RETURN = '''
user_id:
    description: The user id of the user in harbor
    type: integer
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


class HarborUser(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            harbor_domain=dict(type='str', required=True),
            username=dict(type='str', required=True),
            real_name=dict(type='str', required=False),
            email=dict(type='str', required=False),
            password=dict(type='str', required=False, no_log=True),
            state=dict(type='str', required=False, default='present', choices=['present', 'absent']),
        )

        # Module input variables
        self.harbor_domain = None
        self.username = None
        self.email = None
        self.real_name = None
        self.password = None
        self.state = None

        self.results = dict(
            changed=False,
            user_id=None
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

        user_id = self.user_exists()
        self.results['user_id'] = user_id

        if (self.state == 'present' and user_id) or (self.state == 'absent' and user_id is None):
            # DO NOTHING - everything is as it should be
            pass
        elif self.state == 'present' and user_id is None:
            # Validate we have the right data before proceeding to create the user
            if self.email is None or self.password is None or self.real_name is None:
                self.module.fail_json(msg='You need to specify an email, real name and password to create a user')

            self.create_user()
        elif self.state == 'absent' and user_id:
            self.delete_user(user_id)
        else:
            self.module.fail_json(msg='Unknown combination of operations!')

        return self.results

    def create_user(self):
        headers = {
            'Content-Type': 'application/json'
        }

        request_type = 'POST'

        path = '/api/v2.0/users'

        data = {
            'username': self.username,
            'realname': self.real_name,
            'email': self.email,
            'password': self.password,
        }

        resp, info = fetch_url(self.module, self.harbor_domain + path, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 201:
            reason = 'Harbor gave a status code of ' + str(info["status"]) + ' creating the user.'

            if 'body' in info:
                reason += ' Error was: ' + info['body'].decode()

            self.module.fail_json(msg='User create request unsuccessful. ' + reason)

        self.results['changed'] = True

        # Rely on location redirecting to new user in format "/api/v2.0/users/9". We reset here because the user id would
        # have been None when calling this function
        url_parts = info['location'].split("/")
        self.results['user_id'] = url_parts[4]

    def delete_user(self, user_id):
        request_type = 'DELETE'

        path = '/api/v2.0/users/{}'.format(user_id)

        resp, info = fetch_url(self.module, self.harbor_domain + path, method=request_type)

        if info["status"] != 200:
            reason = 'Harbor gave a status code of ' + str(info["status"]) + ' deleting the user'

            self.module.fail_json(msg='User delete request unsuccessful. ' + reason)

        self.results['changed'] = True

    def user_exists(self):
        headers = {
            'Content-Type': 'application/json'
        }

        query = {
            'username': self.username
        }

        request_type = 'GET'
        path = '/api/v2.0/users'
        url = path + '?' + urlencode(query)
        resp, info = fetch_url(self.module, self.harbor_domain + url, headers=headers, method=request_type)

        if info["status"] != 200:
            reason = 'Harbor gave a status code of ' + str(info["status"]) + ' listing existing users'

            self.module.fail_json(msg='User request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())

        # TODO: Check if there are other numbers of items returned and handle appropriately
        if len(decoded_response) == 1:
            return decoded_response[0]['user_id']

        return None


def main():
    HarborUser()


if __name__ == '__main__':
    main()
