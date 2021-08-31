#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_cluster

short_description: This module handles managing rancher clusters

version_added: "1.0"

description:
    - "This nodule creates (or updates) clusters in a given rancher install."

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
            - The name of the cluster to create/update 
        required: true
    rke_template_revision_id:
        description: The ID of the RKE Template Revision to use for the cluster creation

author:
    - Guy
'''

EXAMPLES = '''
- name: Rancher Cluster
  rancher_cluster:
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


class RancherCluster(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            rancher_domain=dict(type='str', required=True),
            api_bearer_token=dict(type='str', required=True),
            name=dict(type='str', required=True),
            rke_template_revision_id=dict(type='str', required=True),
        )

        # Module input variables
        self.rancher_domain = None
        self.api_bearer_token = None
        self.name = None
        self.rke_template_revision_id = None

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

        cluster_info = self.cluster_exists()

        if cluster_info is False:
            self.create_cluster()
        else:
            self.results['cluster_id'] = cluster_info['id']

            if cluster_info['clusterTemplateRevisionId'] != self.rke_template_revision_id:
                self.cluster_upgrade(cluster_info['id'])

        return self.results

    def cluster_upgrade(self, cluster_id):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'PUT'

        data = {
            'name': self.name,
            'clusterTemplateRevisionId': self.rke_template_revision_id
        }

        resp, info = fetch_url(self.module, self.rancher_domain + self.path + cluster_id, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 200:
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' updating ' + str(cluster_id) + ' cluster'

            self.module.fail_json(msg='Cluster Upgrade request unsuccessful. ' + reason)

        self.results['changed'] = True

    def create_cluster(self):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'POST'

        data = {
            'name': self.name,
            'clusterTemplateRevisionId': self.rke_template_revision_id
        }

        resp, info = fetch_url(self.module, self.rancher_domain + self.path, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 201:
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' creating cluster'

            self.module.fail_json(msg='Cluster Create request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())

        self.results['changed'] = True
        self.results['cluster_id'] = decoded_response['id']

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
            return decoded_response['data'][0]

        return False


def main():
    RancherCluster()


if __name__ == '__main__':
    main()
