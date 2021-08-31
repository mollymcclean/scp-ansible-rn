#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_active_directory

short_description: This module manages the active directory configuration for rancher.

version_added: "1.0"

description:
    - This module provisions the active directory configuration for rancher.

options:
    rancher_domain:
        description:
            - The rancher domain name, e.g. rancher.cloudranger.co.uk
        required: true
    api_bearer_token:
        description:
            - The bearer token used to authorise the command.
        required: true
    service_account_username:
        description:
            - The service account username for the active directory configuration.
        required: true
    service_account_password:
        description:
            - The bearer token used to authorise the command.
        required: true
    domain_servers:
        description:
            - The domain servers to use for the authentication.
        required: true
    default_login_domain:
        description:
            - The default domain for users.
        required: true
    group_search_base:
        description:
            - The search base to search for groups in.
        required: true
    user_search_base:
        description:
            - The search base to search for users in.
        required: true
    

author:
    - Guy
'''

EXAMPLES = '''
- name: Rancher UI | Configure the AD Auth
  rancher_active_directory:
    rancher_domain: rancher.cloudranger.co.uk
    api_bearer_token: <BEARER TOKEN>    
    service_account_username: my_sa_username
    service_account_password: my_secret_pw
    domain_servers: my_secret_pw
    default_login_domain: my_secret_pw
    group_search_base: my_secret_pw
    user_search_base: my_secret_pw
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


class RancherActiveDirectory(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            rancher_domain=dict(type='str', required=True),
            access_mode=dict(type='str', required=False, default='restricted'),
            active_directory_allowed_login_principals=dict(type='list', elements='str', required=True),
            api_bearer_token=dict(type='str', required=True),
            service_account_username=dict(type='str', required=True),
            service_account_password=dict(type='str', required=True, no_log=True),
            domain_servers=dict(type='list', elements='str', required=True),
            default_login_domain=dict(type='str', required=True),
            group_search_base=dict(type='str', required=True),
            user_search_base=dict(type='str', required=True),
        )

        # Module input variables
        self.access_mode = None
        self.active_directory_allowed_login_principals = None
        self.rancher_domain = None
        self.api_bearer_token = None
        self.service_account_username = None
        self.service_account_password = None
        self.domain_servers = None
        self.default_login_domain = None
        self.group_search_base = None
        self.user_search_base = None

        # Internal variables that aren't set through the module input
        self.path = '/v3/activeDirectoryConfigs/activedirectory/'

        self.type = 'activeDirectoryConfig'

        self.results = dict(
            changed=False,
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

        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'PUT'

        data = {
            "accessMode": self.access_mode,
            "baseType": "authConfig",
            "allowedPrincipalIds": self.active_directory_allowed_login_principals,
            "connectionTimeout": 5000,
            "defaultLoginDomain": self.default_login_domain,
            "enabled": True,
            "groupDNAttribute": "distinguishedName",
            "groupMemberMappingAttribute": "member",
            "groupMemberUserAttribute": "distinguishedName",
            "groupNameAttribute": "name",
            "groupObjectClass": "group",
            "groupSearchAttribute": "sAMAccountName",
            "groupSearchBase": self.group_search_base,
            "id": "activedirectory",
            "name": "activedirectory",
            "nestedGroupMembershipEnabled": True,
            "port": 389,
            "servers": self.domain_servers,
            "serviceAccountUsername": self.service_account_username,
            "serviceAccountPassword": self.service_account_password,
            "tls": False,
            "type": "activeDirectoryConfig",
            "userDisabledBitMask": 2,
            "userEnabledAttribute": "userAccountControl",
            "userLoginAttribute": "sAMAccountName",
            "userNameAttribute": "name",
            "userObjectClass": "person",
            "userSearchAttribute": "sAMAccountName|sn|givenName",
            "userSearchBase": self.user_search_base
        }

        resp, info = fetch_url(self.module, self.rancher_domain + self.path, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 200:
            reason = 'Rancher gave a status code of ' + str(info["status"])

            self.module.fail_json(msg='Active directory configuration create request unsuccessful. ' + reason)

        return self.results

def main():
    RancherActiveDirectory()


if __name__ == '__main__':
    main()
