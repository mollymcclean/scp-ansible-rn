#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_create_rke_template_version

short_description: RKE template to be used when creating a cluster

version_added: "1.0"

description:
    - "This module creates an empty RKE template."

options:
    name:
        description:
            - The name of the RKE Template
        required: true


author:
    - Guy
'''

EXAMPLES = '''
- name: Rancher RKE Template Creation
  rancher_create_rke_template:
    rancher_domain: example.com
    api_bearer_token: token_export
    name: My Cluster Template

'''

RETURN = '''
rke_template_id:
    description: The unique identifier for the RKE template
    type: string
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json

class RancherRKETemplate(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            api_bearer_token=dict(type='str', required=True),
            rancher_domain=dict(type='str', required=True),
            name=dict(type='str', required=True),
        )

        # Module input variables
        self.api_bearer_token = None
        self.rancher_domain = None
        self.name = None

        # Internal variables that aren't set through the module input
        self.path = '/v3/clusterTemplate'

        self.results = dict(
            changed=False,
            rke_template_id='',
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

        rke_template_id = self.template_exists()

        if rke_template_id is False:
            self.create_rke_template()
        else:
            self.results['rke_template_id'] = rke_template_id

        return self.results

    def create_rke_template(self):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'POST'

        data = {
           "name": self.name
        }

        resp, info = fetch_url(self.module, self.rancher_domain + self.path, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 201:
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' creating an RKE template'

            self.module.fail_json(msg='RKE Template Create request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())

        self.results['changed'] = True
        self.results['rke_template_id'] = decoded_response['id']

    def template_exists(self):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        query = {
            'name': self.name
        }

        request_type = 'GET'
        url = self.path + '?' + urlencode(query)
        resp, info = fetch_url(self.module, self.rancher_domain + url, headers=headers, method=request_type)

        if info["status"] != 200:
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' listing existing templates'

            self.module.fail_json(msg='RKE Template List request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())
        items = len(decoded_response['data'])

        # TODO: Check if there are other numbers of items returned and handle appropriately
        if items == 1:
            return decoded_response['data'][0]['id']

        return False


def main():
    RancherRKETemplate()


if __name__ == '__main__':
    main()
