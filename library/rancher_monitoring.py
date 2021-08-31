#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_monitoring

short_description: This module manages monitoring configuration for Rancher.

version_added: "1.0"

description:
    - This module provisions monitoring configuration for Rancher clusters
    - Configuration defaults match defaults from the Rancher UI

options:
    rancher_domain:
        description:
            - The Rancher domain name, e.g. rancher.cloudranger.co.uk
        required: true
    rancher_cluster_id:
        description:
            - The unique string ID of the Rancher cluster to modify
            - Use the rancher_cluster_info module to find this from the cluster
              name if required
        required: true
    api_bearer_token:
        description:
            - The bearer token used to authorise the command.
        required: true
    enable_monitoring:
        description:
            - Whether or not monitoring should be enabled
        type: bool
        required: true
    grafana_persistence_enabled:
        description:
            - Whether or not to configure a persistent volume for Grafana
            - If disabled, metrics will be stored per-pod and will be lost if a
              pod fails or is killed.
        type: bool
        required: false
        default: 'no'
    grafana_persistence_size:
        description:
            - Size of PV for Grafana persistence, if enabled.
        required: false
        default: '10Gi'
    grafana_persistence_storageclass:
        description:
            - Storage class for Grafana persistent storage, if enabled.
        required: false
        default: 'default'
    node_exporter_kubelets_https:
        description:
            - Whether or not the node exporter should use HTTPS to communicate
              with node kubelets.
        type: bool
        required: false
        default: 'yes'
    node_exporter_enabled:
        description:
            - Whether or not to enable the Prometheus node exporter.
            - If enabled, the node exporter will be deployed in hostNetwork mode.
        type: bool
        required: false
        default: 'yes'
    node_exporter_metrics_port:
        description:
            - Port on each node that Prometheus should use to collect metrics
              from the node exporter.
        required: false
        default: '9796'
    node_exporter_cpu_limit:
        description:
            - CPU limit for the node exporter. Kubernetes format.
        required: false
        default: '200m'
    node_exporter_memory_limit:
        description:
            - Memory limit for the node exporter. Kubernetes format.
        required: false
        default: '200Mi'
    operator_init_container_enabled:
        description:
            - Whether or not to enable adding init containers to the Prometheus
              operator.
            - The upstream prometheus-operator project supports this as a way of
              injecting secrets into Prometheus
        type: bool
        required: false
        default: 'yes'
    operator_memory_limit:
        description:
            - Memory limit for the Prometheus operator. Kubernetes format.
        required: false
        default: '500Mi'
    prometheus_persistence_enabled:
        description:
            - Whether or not to configure a persistent volume for Prometheus
            - If disabled, metrics will be stored per-pod and will be lost if a
              pod fails or is killed.
        type: bool
        required: false
        default: 'no'
    prometheus_persistence_size:
        description:
            - Size of PV for Prometheus persistence, if enabled.
        required: false
        default: '50Gi'
    prometheus_persistence_storageclass:
        description:
            - Storage class for Prometheus persistent storage, if enabled.
        required: false
        default: 'default'
    prometheus_persistence_use_releasename:
        description:
            - Use a shorter name for PVs created when enabling persistence for
              Prometheus.
            - This seems to have been introduced to work around length limits in
              PV names from some providers.
        required: false
        default: 'yes'
    prometheus_core_cpu_limit:
        description:
            - CPU limit for core Prometheus components. Kubernetes format.
        required: false
        default: '1000m'
    prometheus_core_memory_limit:
        description:
            - Memory limit for core Prometheus components. Kubernetes format.
        required: false
        default: '1000Mi'
    prometheus_core_cpu_request:
        description:
            - CPU request for core Prometheus components. Kubernetes format.
        required: false
        default: '750m'
    prometheus_core_memory_request:
        description:
            - Memory request for core Prometheus components. Kubernetes format.
        required: false
        default: '750Mi'
    prometheus_retention:
        description:
            - Retention time for Prometheus data
        required: false
        default: '12h'

notes:
    - This module supports check mode, but will throw errors if the Rancher
      cluster being targeted does not exist when check mode is run.
    - If you need to avoid this, consider appending
      'ignore_errors: "{{ ansible_check_mode }}"' to your task definition.


author:
    - Guy
'''

EXAMPLES = '''
- name: Rancher cluster | Ensure monitoring is disabled
  rancher_monitoring:
    rancher_domain: rancher.cloudranger.co.uk
    rancher_cluster_id: <CLUSTER ID>
    api_bearer_token: <BEARER TOKEN>    
    enable_monitoring: no

- name: Rancher cluster | Configure monitoring
  rancher_monitoring:
    rancher_domain: rancher.cloudranger.co.uk
    rancher_cluster_id: <CLUSTER ID>
    api_bearer_token: <BEARER TOKEN>    
    enable_monitoring: yes
    grafana_persistence_enabled: yes
    prometheus_persistence_enabled: yes
    prometheus_persistence_size: 64Gi
    prometheus_retention: 24h
    ignore_errors: "{{ ansible_check_mode }}"
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


class RancherMonitoring(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            rancher_domain=dict(type='str', required=True),
            rancher_cluster_id=dict(type='str', required=True),
            api_bearer_token=dict(type='str', required=True),
            enable_monitoring=dict(type='bool', required=True),
            # End of required arguments. Defaults below are from the Rancher UI
            grafana_persistence_enabled=dict(type='bool', default=False),
            grafana_persistence_size=dict(type='str', default='10Gi'),
            grafana_persistence_storageclass=dict(type='str', default='default'),
            node_exporter_kubelets_https=dict(type='bool', default=True),
            node_exporter_enabled=dict(type='bool', default=True),
            node_exporter_metrics_port=dict(type='str', default='9796'),
            node_exporter_cpu_limit=dict(type='str', default='200m'),
            node_exporter_memory_limit=dict(type='str', default='200Mi'),
            operator_memory_limit=dict(type='str', default='500Mi'),
            prometheus_persistence_enabled=dict(type='bool', default=False),
            prometheus_persistence_size=dict(type='str', default='50Gi'),
            prometheus_persistence_storageclass=dict(type='str', default='default'),
            prometheus_persistence_use_releasename=dict(type='bool', default=True),
            prometheus_core_cpu_limit=dict(type='str', default='1000m'),
            prometheus_core_memory_limit=dict(type='str', default='1000Mi'),
            prometheus_core_cpu_request=dict(type='str', default='750m'),
            prometheus_core_memory_request=dict(type='str', default='750Mi'),
            prometheus_retention=dict(type='str', default='12h')
        )

        # Version argument to the API call that enables monitoring
        # Not exposed to users as Rancher's docs are not clear on what other
        # values this can take, if any.
        #
        # Possibly it is versioning the set of available configuration options
        self._version = '0.1.0'

        # The 'operator-init.enabled' flag is not exposed via the UI or
        # obviously documented anywhere
        # It probably maps to the initContainer flag on the upstream
        # prometheus-operator project:
        # https://github.com/coreos/prometheus-operator/blame/c0fcbc4b7614d0f90a97cc9eee63facfbca6d700/Documentation/api.md#L164
        self._operator_init_enabled = True

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

        self.http_headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        if not self.enable_monitoring:
            self.rancher_disable_monitoring()
        else:
            existing_config = self.get_current_monitoring_settings()
            if existing_config: # Monitoring is already enabled
                if self.config_changes_needed(
                        existing_config,
                        self.build_request_data()
                ):
                    self.rancher_edit_monitoring()
                else:
                    return self.results
            else:
                self.rancher_enable_monitoring()

        return self.results

    def build_request_data(self):
        '''
        Helper method to take module arguments and turn them into valid API JSON
        Returns a JSON string suitable for POST-ing directly to the Rancher API
        '''
        data = {
            "answers": {
                "exporter-kubelets.https": self.node_exporter_kubelets_https,
                "exporter-node.enabled": self.node_exporter_enabled,
                "exporter-node.ports.metrics.port": self.node_exporter_metrics_port,
                "exporter-node.resources.limits.cpu": self.node_exporter_cpu_limit,
                "exporter-node.resources.limits.memory": self.node_exporter_memory_limit,
                "grafana.persistence.enabled": self.grafana_persistence_enabled,
                "grafana.persistence.size": self.grafana_persistence_size,
                "grafana.persistence.storageClass": self.grafana_persistence_storageclass,
                "operator-init.enabled": self._operator_init_enabled,
                "operator.resources.limits.memory": self.operator_memory_limit,
                "prometheus.persistence.enabled": self.prometheus_persistence_enabled,
                "prometheus.persistence.size": self.prometheus_persistence_size,
                "prometheus.persistence.storageClass": self.prometheus_persistence_storageclass,
                "prometheus.persistent.useReleaseName": self.prometheus_persistence_use_releasename,
                "prometheus.resources.core.limits.cpu": self.prometheus_core_cpu_limit,
                "prometheus.resources.core.limits.memory": self.prometheus_core_memory_limit,
                "prometheus.resources.core.requests.cpu": self.prometheus_core_cpu_request,
                "prometheus.resources.core.requests.memory": self.prometheus_core_memory_request,
                "prometheus.retention": self.prometheus_retention,
            },
            "version": self._version,
        }

        # The Rancher API doesn't want real JSON, it wants booleans as lowercase strings
        for key, val in data['answers'].items():
            if isinstance(val, bool):
                data['answers'][key] = str(val).lower()

        return json.dumps(data)

    @staticmethod
    def config_changes_needed(existing, desired):
        '''
        Helper method to compare existing cluster config with desired config
        Returns True if configurations differ, otherwise False
        '''
        existing = json.loads(existing)
        desired = json.loads(desired)
        if existing['answers'] != desired['answers']:
            return True
        if existing['version'] != desired['version']:
            return True
        return False

    def rancher_enable_monitoring(self):
        '''
        Enables monitoring config on the remote cluster
        If successful, 'changed' is always true and self.results is modified

        Returns self.results
        '''

        if self.module.check_mode:
            self.results["changed"] = True
            return self.results

        resp, info = self.rancher_api_request(
            'enableMonitoring',
            self.build_request_data()
        )

        if info["status"] != 204:
            reason = 'Rancher gave a status code of %s, expected 204' % str(info["status"])
            self.module.fail_json(msg='Request to enable or update monitoring was unsuccessful. ' + reason)

        self.results['changed'] = True
        return self.results

    def rancher_edit_monitoring(self):
        '''
        Edits monitoring config on the remote cluster
        If successful, 'changed' is always true and self.results is modified

        Returns self.results
        '''

        if self.module.check_mode:
            self.results["changed"] = True
            return self.results

        resp, info = self.rancher_api_request(
            'editMonitoring',
            self.build_request_data()
        )

        if info["status"] != 204:
            reason = 'Rancher gave a status code of %s, expected 204' % str(info["status"])
            self.module.fail_json(msg='Request to enable or update monitoring was unsuccessful. ' + reason)

        self.results['changed'] = True
        return self.results

    def rancher_disable_monitoring(self):
        '''
        Disables monitoring on the remote cluster and updates self.results if
        anything was changed

        Returns self.results
        '''

        existing_config = self.get_current_monitoring_settings()
        if existing_config:
            if self.module.check_mode:
                self.results["changed"] = True
                return self.results

            resp, info = self.rancher_api_request(endpoint='disableMonitoring')

            if info["status"] == 204:
                self.results['changed'] = True
            else:
                reason = 'Rancher gave a status code of %s, expected 204' % str(info["status"])
                self.module.fail_json(msg='Request to disable monitoring was unsuccessful. ' + reason)

        return self.results

    def get_current_monitoring_settings(self):
        '''
        Checks if monitoring is enabled on the remote cluster
        Returns a dict with current settings, or False if it is not enabled
        '''

        response, info = self.rancher_api_request(endpoint='viewMonitoring')

        if info["status"] == 200:
            return response.read()
        elif info["status"] == 422:
            return False
        else:
            reason = 'Rancher gave a status code of %s, expected 200 or 422' % str(info["status"])
            self.module.fail_json(msg='Request to disable monitoring was unsuccessful. ' + reason)

    def rancher_api_request(self, endpoint, data=None):

        path = '/v3/clusters/%s?action=%s' % (self.rancher_cluster_id,
                                              endpoint)
        response, info = fetch_url(
            self.module,
            self.rancher_domain + path,
            data=data,
            headers=self.http_headers,
            method='POST'
        )
        return (response, info)


def main():
    RancherMonitoring()


if __name__ == '__main__':
    main()
