#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_cluster_info

short_description: This module handles managing rancher clusters

version_added: "1.0"

description:
    - "This nodule outputs the cluster id for a named cluster"

options:
    rancher_domain:
        description:
            - The Name of the rancher domain
        required: true
    api_bearer_token:
        description:
            - The rancher bearer token to authenticate with 
        required: true
    name:
        description:
            - The name of the cluster to retrieve
        required: true

author:
    - Guy
'''

EXAMPLES = '''
- name: Rancher Cluster
  rancher_cluster_info:
    rancher_domain: rancher.cloudranger.co.uk
    api_bearer_token: token_export
    name: My Cluster Name
'''

RETURN = '''
cluster_id:
    description: The unique identifier for the cluster
    type: string
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


class RancherClusterInfo(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            rancher_domain=dict(type='str', required=True),
            api_bearer_token=dict(type='str', required=True),
            name=dict(type='str', required=True),
        )

        # Module input variables
        self.rancher_domain = None
        self.api_bearer_token = None
        self.name = None

        # Internal variables that aren't set through the module input
        self.path = '/v3/clusters/'

        self.results = dict(
            changed=False,
            cluster_id='',
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

        cluster_id = self.cluster_exists()

        if cluster_id is False:
            self.module.fail_json(msg='Unable to find cluster')
        else:
            self.results['cluster_id'] = cluster_id

        return self.results

    def cluster_exists(self):
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
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' listing existing clusters'

            self.module.fail_json(msg='Cluster request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())

        # TODO: Check if there are other numbers of items returned and handle appropriately
        if len(decoded_response['data']) == 1:
            return decoded_response['data'][0]['id']

        return False


def main():
    RancherClusterInfo()


if __name__ == '__main__':
    main()
