#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_manage_nodepool

short_description: This module manages the nodepools of a cluster.

version_added: "1.0"

description:
    - This module manages a nodepool of a cluster. There are three types of nodepool: Control Plane, etcd, Worker. When a cluster is created, a nodepool of each type is usually created. This will result in three commands being executed by this module.

options:
    rancher_domain:
        description:
            - The rancher domain name, e.g. rancher.cloudranger.co.uk
        required: true
    api_bearer_token:
        description:
            - The bearer token used to authorise the command.
        required: true
    control_plane:
        description:
            - Set to "true" if the nodepool defines control plane hosts.
        required: true
    control_plane_quantity:
        description:
            - The number of control hosts in the nodepool.
        required: true
    control_plane_nodepool_prefix:
        description:
            - The pre-fix to use for each host in the control nodepool.
        required: true
    delete_not_ready_after_secs:
        description:
            - The number of seconds before the hosts in the nodepool are deleted if not ready.
        required: true
    display_name:
        description:
            - The display name for the node pool.
        required: false
    etcd:
        description:
            - Set to "true" if the nodepool defines etcd hosts.
        required: true
    etcd_quantity:
        description:
            - The number of etcd hosts in the nodepool. 
        required: true
    etcd_nodepool_prefix:
        description:
            - The pre-fix to use for each host in the etcd nodepool.
        required: true
    node_pool_name_prefix:
        description:
            - The prefix to use for the node pool resource (not shown in the UI but used to ensure unique node pools)
        required: true
    worker:
        description:
            - Set to "true" if the nodepool defines worker hosts.
        required: true
    worker_quantity:
        description:
            - The number of worker hosts in the nodepool. 
        required: true
    worker_nodepool_prefix:
        description:
            - The pre-fix to use for each host in the worker nodepool.
        required: true
    type:
        description:
            - Always set to "nodePool".
        required: true
    cluster_id:
        description:
            - The ID of the cluster to add/update/delete the nodepool to/in/from.
        required: true
    node_template_id:
        description:
            - The ID of the template to use building the cluster.
        required: true
    worker_node_template_id:
        description:
            - The ID of the worker role node template to use building the cluster.
        required: true
    

author:
    - Guy
'''

EXAMPLES = '''
- name: RKE Nodepool | Add nodepools to cluster
  rancher_manage_nodepool:
    rancher_domain: rancher.cloudranger.co.uk
    api_bearer_token: <BEARER TOKEN>
    delete_not_ready_after_secs: 0
    control_plane: true
    control_plane_quantity: 2
    etcd: true
    etcd_quantity: 3
    worker: false
    worker_quantity: 1
    type: nodePool
    cluster_id: <cluster ID>
    control_plane_nodepool_prefix: cis-cntl
    etcd_nodepool_prefix: cis-etcd
    worker_nodepool_prefix: cis-wrkr
    node_template_id: cattle-global-nt:nt-8t9xc
    worker_node_template_id: cattle-global-nt:nt-8t9xc
    
'''

RETURN = '''
# user_id:
#     description: The user id of the user in harbor
#     type: integer
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


class RancherClusterNodePool(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            rancher_domain=dict(type='str', required=True),
            api_bearer_token=dict(type='str', required=True),
            control_plane=dict(type='bool', default=False),
            control_plane_quantity=dict(type='int', default=0),
            control_plane_nodepool_prefix=dict(type='str', required=True),
            control_plane_node_template_id=dict(type='str', required=True),
            display_name=dict(type='str', required=False),
            etcd=dict(type='bool', default=False),
            etcd_quantity=dict(type='int', default=0),
            etcd_nodepool_prefix=dict(type='str', required=True),
            etcd_node_template_id=dict(type='str', required=True),
            node_pool_name_prefix=dict(type='str', required=True),
            worker=dict(type='bool', default=False),
            worker_quantity=dict(type='int', default=0),
            worker_nodepool_prefix=dict(type='str', required=True),
            worker_node_template_id=dict(type='str', required=True),
            delete_not_ready_after_secs=dict(type='int', default=0),
            type=dict(type='str', default='nodePool'),
            cluster_id=dict(type='str', required=True),
        )

        # Module input variables
        self.rancher_domain = None
        self.api_bearer_token = None
        self.control_plane = None
        self.control_plane_quantity = None
        self.control_plane_nodepool_prefix = None
        self.control_plane_node_template_id = None
        self.display_name = None
        self.etcd = None
        self.etcd_quantity = None
        self.etcd_nodepool_prefix = None
        self.etcd_node_template_id = None
        self.worker = None
        self.worker_quantity = None
        self.worker_nodepool_prefix = None
        self.worker_node_template_id = None
        self.delete_not_ready_after_secs = None
        self.type = None
        self.cluster_id = None
        self.node_pool_name_prefix = None

        # Internal variables that aren't set through the module input
        self.path = '/v3/nodepool/'

        self.type = 'nodePool'

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

        control_plane_node_pool_name = self.node_pool_name_prefix + '-cp'
        worker_node_pool_name = self.node_pool_name_prefix + '-worker'
        etcd_node_pool_name = self.node_pool_name_prefix + '-etcd'

        # Execute all three nodepool creation commands:
        if self.control_plane_quantity > 0 and not self.nodepool_exists(control_plane_node_pool_name):
            self.create_control_plane_nodepool(control_plane_node_pool_name)

        if self.etcd_quantity > 0 and not self.nodepool_exists(etcd_node_pool_name):
            self.create_etcd_nodepool(etcd_node_pool_name)

        if self.worker_quantity > 0 and not self.nodepool_exists(worker_node_pool_name):
            self.create_worker_nodepool(worker_node_pool_name)

        return self.results

    def create_control_plane_nodepool(self, name):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'POST'

        path = '/v3/nodePool/'

        data = {
            'controlPlane': self.control_plane,
            'displayName': self.display_name,
            'etcd': False,
            'worker': False,
            'quantity': self.control_plane_quantity,
            'deleteNotReadyAfterSecs': self.delete_not_ready_after_secs,
            'type': self.type,
            'clusterId': self.cluster_id,
            'hostnamePrefix': self.control_plane_nodepool_prefix,
            'nodeTemplateId': self.control_plane_node_template_id,
            'name': name,
        }

        resp, info = fetch_url(self.module, self.rancher_domain + path, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 201:
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' creating control plane nodepool'

            self.module.fail_json(msg='Control plane nodepool create request unsuccessful. ' + reason)

        self.results['changed'] = True

    def create_etcd_nodepool(self, name):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'POST'

        path = '/v3/nodePool/'

        data = {
            'controlPlane': False,
            'displayName': self.display_name,
            'etcd': self.etcd,
            'worker': False,
            'quantity': self.etcd_quantity,
            'deleteNotReadyAfterSecs': self.delete_not_ready_after_secs,
            'type': self.type,
            'clusterId': self.cluster_id,
            'hostnamePrefix': self.etcd_nodepool_prefix,
            'nodeTemplateId': self.etcd_node_template_id,
            'name': name,
        }

        resp, info = fetch_url(self.module, self.rancher_domain + path, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 201:
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' creating etcd nodepool'

            self.module.fail_json(msg='etcd nodepool create request unsuccessful. ' + reason)

        self.results['changed'] = True

    def create_worker_nodepool(self, name):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'POST'

        path = '/v3/nodePool/'

        data = {
            'controlPlane': False,
            'displayName': self.display_name,
            'etcd': False,
            'worker': self.worker,
            'quantity': self.worker_quantity,
            'deleteNotReadyAfterSecs': self.delete_not_ready_after_secs,
            'type': self.type,
            'clusterId': self.cluster_id,
            'hostnamePrefix': self.worker_nodepool_prefix,
            'nodeTemplateId': self.worker_node_template_id,
            'name': name,
        }

        resp, info = fetch_url(self.module, self.rancher_domain + path, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 201:
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' creating worker nodepool'

            self.module.fail_json(msg='Worker nodepool create request unsuccessful. ' + reason)

        self.results['changed'] = True

    def nodepool_exists(self, name):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        query = {
            'name': name
        }

        request_type = 'GET'
        path = '/v3/nodePool/'
        url = path + '?' + urlencode(query)
        resp, info = fetch_url(self.module, self.rancher_domain + url, headers=headers, method=request_type)

        if info["status"] != 200:
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' listing existing nodepool'

            self.module.fail_json(msg='Nodepool list request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())
        items = len(decoded_response['data'])

        if items == 1:
            return True

        return False

def main():
    RancherClusterNodePool()


if __name__ == '__main__':
    main()
