#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_vsphere_cloud_credentials

version_added: "1.0"

description: 
    - Ensures a set of cloud credentials exist in Rancher using the given credential name"
    - NB: Will not update existing credentials

options:
    rancher_domain:
        description:
            - The URL or the Rancher UI
        required: true
    api_bearer_token:
        description:
            - The Rancher bearer token to authenticate with
        required: true
    cloud_credentials_name:
        description:
            - The name of the cloud credentials to get or set
        required: true
    vsphere_domain:
        description:
            - The domain name to use for vSphere
        required: true
    vsphere_port:
        description:
            - The port to use for vSphere
        required: false
        default: "443"
    vsphere_username:
        description:
            - The username for the vSphere account for the cloud credentials
        required: true
    vsphere_password:
        description:
            - The password for the vSphere account for the cloud credentials
        required: true

author:
    - Guy
'''

EXAMPLES = '''
- name: Set cloud credentials
  rancher_vsphere_cloud_credentials:
    rancher_domain: rancher.cloudranger.co.uk
    api_bearer_token: token_export
    credentials_name: my_credentials
    vsphere_domain: rnvcenter.lab.int
    vsphere_username: foo
    vsphere_password: bar
  register: cloud_credentials

- name: Task that uses cloud credentials
  my_other_task:
    rancher_cloud_credentials: cloud_credentials.id
'''

RETURN = '''
id:
    description: The ID of the matching cloud credentials within Rancher
    type: string
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json

class RancherVsphereCredentials(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            rancher_domain=dict(type='str', required=True),
            api_bearer_token=dict(type='str', required=True),
            credentials_name=dict(type='str', required=True),
            vsphere_domain=dict(type='str', required=True),
            vsphere_username=dict(type='str', required=True),
            vsphere_password=dict(type='str', required=True),
            vsphere_port=dict(type='str', default="443"),
        )

        # Module input variables
        self.rancher_domain = None
        self.api_bearer_token = None
        self.credentials_name = None
        self.vsphere_domain = None
        self.vsphere_username = None
        self.vsphere_password = None
        self.vsphere_port = None

        # Internal variables that aren't set through the module input
        self.results = dict(
            changed=False,
            id='',
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

        self.results = self.get_or_set_cloud_credentials()

        if self.results["id"] is False:
            self.module.fail_json(msg='Unable to read from credentials')
        else:
            return self.results

    def get_or_set_cloud_credentials(self):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'GET'
        path = '/v3/cloudcredentials'
        resp, info = fetch_url(self.module, self.rancher_domain + path, headers=headers, method=request_type)

        if info["status"] != 200:
            reason = 'Rancher gave a system code of ' + str(info["status"]) + ' listing existing credentials'
            self.module.fail_json(msg='Cluster request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())

        for credential in decoded_response["data"]:
            # Rancher does not expose all credential fields (in order to protect passwords)
            # and so we cannot safely check if the credentials requires any update.
            #
            # To work around this, we return the ID of the first credential with matching name and type.
            # If passwords need to be updated it must be done manually or by deleting the old credential
            if credential["name"] == self.credentials_name and "vmwarevspherecredentialConfig" in credential.keys():
                return { "changed": False, "id": credential["id"] }

        # If no credentials with matching name are found
        return { "changed": True, "id": self.create_new_credentials() }

    def create_new_credentials(self):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }
        data = {
            "type": "cloudCredential",
            "name": self.credentials_name,
            "vmwarevspherecredentialConfig": {
                "username": self.vsphere_username,
                "password": self.vsphere_password,
                "vcenter": self.vsphere_domain,
                "vcenterPort": self.vsphere_port,
            }
        }

        request_type = 'POST'
        path = '/v3/cloudcredential'
        resp, info = fetch_url(self.module, self.rancher_domain + path, headers=headers, method=request_type, data=json.dumps(data))

        if info["status"] >= 300:
            reason = 'Rancher gave a status code of ' + str(info("status")) + ' when attempting to add new credentials'
            self.module.fail_json(msg='Cluster request unsuccessful, ' + reason)
        
        decoded_response = json.loads(resp.read())
        return decoded_response["id"]

def main():
    RancherVsphereCredentials()

if __name__ == '__main__':
    main()