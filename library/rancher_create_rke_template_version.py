#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_create_rke_template

short_description: RKE template to be used when creating a cluster

version_added: "1.0"

description:
    - "This module creates an RKE template version to be used when creating a cluster."

options:
    cluster_config_default_cluster_role_for_project_members: 
        description: 
            - 
        required: 
    cluster_config_default_pod_security_policy_template_id: 
        description: 
            - 
        required: 
    cluster_config_enable_cluster_alerting: 
        description: 
            - 
        required: 
    cluster_config_enable_cluster_monitoring: 
        description: 
            - 
        required: 
    cluster_config_enable_network_policy: 
        description: 
            - 
        required: 
    cluster_config_local_cluster_auth_endpoint_enabled: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_addon_job_timeout: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_authentication_strategy: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_cloud_provider_name: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_custom_addons: 
        description: 
            - Custom YAML to be applied to a Kubernetes cluster
        required:
    cluster_config_rancher_kubernetes_engine_config_ignore_docker_version: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_ingress_provider: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_ingress_extra_args: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_ingress_options: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_kubernetes_version: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_monitoring_provider: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_network_mtu: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_network_options_flannel_backend_type: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_network_plugin: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_private_registries:
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_enabled: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_intervalHours: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_retention: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_safe_timestamp: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_creation: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_extra_args_election_timeout: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_extra_args_heartbeat_interval: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_gid: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_retention: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_snapshot: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_etcd_uid: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_kube_api_always_pull_images: 
        description: 
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_kube_api_audit_log_enabled:
        description:
            - Whether or not to enable the API audit log
        required: false
        default: true
    cluster_config_rancher_kubernetes_engine_config_services_kube_api_event_rate_limit_enabled:
        description:
            - Whether or not to rate limit API events
        required: false
        default: true
    cluster_config_rancher_kubernetes_engine_config_services_kube_api_pod_security_policy: 
        description:
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_kube_api_secrets_encryption_config_enabled:
        description:
            - Whether or not to encrypt secrets at rest
        required: false
        default: true
    cluster_config_rancher_kubernetes_engine_config_services_kube_api_service_node_port_range: 
        description:
            - 
        required: 
    cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_anonymous_auth:
        description:
            - Whether or not anonymous auth should be enabled
        required: false
        default: false
    cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_protect_kernel_defaults:
        description:
            - Whether or not the kubelet should enforce verification of kernel defaults with an error
            - If true, the kubelet will error and quit if certain kernel settings are incorrect or are changed
            - If false, the kubelet will attempt to correct them on startup but may not verify them continuously
        required: false
        default: true
    cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_make_iptables_util_chains:
        description:
            - Whether or not the kubelet should create iptables utility rules on each node
            - These have various functions including dropping some invalid or malformed traffic
        required: false
        default: true
    cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_streaming_connection_idle_timeout:
        description:
            - Timeout for idle connections to the kubelet
        required: false
        default: "1800s"
    cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_tls_cipher_suites:
        description:
            - Set of cipher suites enabled for use with the kubelet
        required: false
    cluster_config_rancher_kubernetes_engine_config_services_scheduler_extra_args_address:
        description:
            - Bind address for kube-scheduler
        required: false
        default: 127.0.0.1
    cluster_config_rancher_kubernetes_engine_config_services_scheduler_extra_args_profiling:
        description:
            - Whether to enable scheduler profiling via web interface host:port/debug/pprof/
        required: false
        default: false
    cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_address:
        description:
            - Bind address for kube-controller-manager
        required: false
        default: 127.0.0.1
    cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_profiling:
        description:
            - Whether to enable controller-manager profiling via web interface host:port/debug/pprof/
        required: false
        default: false
    cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_terminated_pod_gc_threshold:
        description:
            - How many terminated pods to tolerate before starting garbage collection
        required: false
        default: "1000"
    cluster_config_rancher_kubernetes_engine_config_ssh_agent_auth: 
        description: 
            - 
        required: 
    cluster_config_windows_prefered_cluster: 
        description: 
            - Is this a windows cluster
        required: false
    cluster_template_id: 
        description: 
            - 
        required: 
    enabled: 
        description: 
            - 
        required: 
    name: 
        description: 
            - 
        required: 


author:
    - Guy
'''

EXAMPLES = '''
- name: Rancher RKE Template Creation
  rancher_create_rke_template:
    rancher_domain: rancher.cloudranger.co.uk
    api_bearer_token: token_export
    default_cluster_role_for_project_members: null
    default_pod_security_policy_template_id: null
    docker_root_dir: "/var/lib/docker
    enable_cluster_alerting: false
    enable_cluster_monitoring: false
    enable_network_policy: true
    local_cluster_auth_endpoint_enabled: false
    rancher_kubernetes_engine_config_addon_job_timeout: 30
    rancher_kubernetes_engine_config_authentication_strategy: x509
    rancher_kubernetes_engine_config_cloud_provider_name: aws
    rancher_kubernetes_engine_config_ignore_docker_version: true
    rancher_kubernetes_engine_config_ingress_provider: nginx
    rancher_kubernetes_engine_config_kubernetes_version: 1.17.x
    rancher_kubernetes_engine_config_monitoring_provider: metrics-server
    rancher_kubernetes_engine_config_network_mtu: 0
    rancher_kubernetes_engine_config_network_options_flannel_backend_type: vxlan
    rancher_kubernetes_engine_config_network_plugin: canal
    rancher_kubernetes_engine_config_private_registries:
    - url: harbor.lab.int
      user: rke_user
      isDefault: yes
    rancher_kubernetes_engine_config_services_etcd_backup_config_enabled: true
    rancher_kubernetes_engine_config_services_etcd_backup_config_intervalHours: 12
    rancher_kubernetes_engine_config_services_etcd_backup_config_retention: 6
    rancher_kubernetes_engine_config_services_etcd_backup_config_safe_timestamp: false
    rancher_kubernetes_engine_config_services_etcd_creation: 12h
    rancher_kubernetes_engine_config_services_etcd_extra_args_election_timeout: 5000
    rancher_kubernetes_engine_config_services_etcd_extra_args_heartbeat_interval: 500
    rancher_kubernetes_engine_config_services_etcd_gid: 0
    rancher_kubernetes_engine_config_services_etcd_retention: 72h
    rancher_kubernetes_engine_config_services_etcd_snapshot: false
    rancher_kubernetes_engine_config_services_etcd_uid: 0
    rancher_kubernetes_engine_config_services_kube_api_always_pull_images: false
    rancher_kubernetes_engine_config_services_kube_api_pod_security_policy: false
    rancher_kubernetes_engine_config_services_kube_api_service_node_port_range: 30000-32767
    rancher_kubernetes_engine_config_ssh_agent_auth: false
    type: /v3/schemas/clusterSpecBase
    windows_prefered_cluster: false
    cluster_template_id: cattle-global-data:ct-qnznw
    enabled: null
    version_name: "v1"

'''

RETURN = '''
rke_revision_id:
    description: The unique identifier for the RKE template revision
    type: string
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json

class RancherRKETemplateVersion(object):
    def __init__(self):
        self.module_spec = url_argument_spec()

        self.tls_cipher_suite_string = (
            "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,"
            "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,"
            "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,"
            "TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256"
        )

        self.module_spec.update(
            api_bearer_token=dict(type='str', required=True),
            cluster_config_default_cluster_role_for_project_members=dict(type='str', required=False, default=None),
            cluster_config_default_pod_security_policy_template_id=dict(type='str', required=False, default="restricted"),
            cluster_config_docker_root_dir=dict(type='str', default='/var/lib/docker'),
            cluster_config_enable_cluster_alerting=dict(type='bool', default=False),
            cluster_config_enable_cluster_monitoring=dict(type='bool', default=False),
            cluster_config_enable_network_policy=dict(type='bool', default=True),
            cluster_config_local_cluster_auth_endpoint_enabled=dict(type='bool', default=True),
            cluster_config_rancher_kubernetes_engine_config_addon_job_timeout=dict(type='int', default="30"),
            cluster_config_rancher_kubernetes_engine_config_authentication_strategy=dict(type='str', required=True),
            cluster_config_rancher_kubernetes_engine_config_cloud_provider_name=dict(type='str', required=True),
            cluster_config_rancher_kubernetes_engine_config_custom_addons=dict(type='str', default=''),
            cluster_config_rancher_kubernetes_engine_config_ignore_docker_version=dict(type='bool', default=True),
            cluster_config_rancher_kubernetes_engine_config_ingress_provider=dict(type='str', required=True),
            cluster_config_rancher_kubernetes_engine_config_ingress_extra_args=dict(type='dict', default={}),
            cluster_config_rancher_kubernetes_engine_config_ingress_options=dict(type='dict', default={}),
            cluster_config_rancher_kubernetes_engine_config_kubernetes_version=dict(type='str', required=True),
            cluster_config_rancher_kubernetes_engine_config_monitoring_provider=dict(type='str', required=True),
            cluster_config_rancher_kubernetes_engine_config_network_mtu=dict(type='int', default="0"),
            cluster_config_rancher_kubernetes_engine_config_network_options_flannel_backend_type=dict(type='str', required=True),
            cluster_config_rancher_kubernetes_engine_config_network_plugin=dict(type='str', required=True),
            cluster_config_rancher_kubernetes_engine_config_private_registries=dict(type='list', required=False, default=None),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_enabled=dict(type='bool', default=True),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_intervalHours=dict(type='int', default="12"),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_retention=dict(type='int', default="6"),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_safe_timestamp=dict(type='bool', default=False),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_creation=dict(type='str', required=True),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_extra_args_election_timeout=dict(type='int', default="5000"),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_extra_args_heartbeat_interval=dict(type='int', default="500"),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_gid=dict(type='int', default="52034"),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_retention=dict(type='str', required=True),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_snapshot=dict(type='bool', default=False),
            cluster_config_rancher_kubernetes_engine_config_services_etcd_uid=dict(type='int', default="52034"),
            # This default deliberately doesn't follow CIS Guidelines 1.2.12 (version 1.5.1) as we are not in a
            # multi-tenanted network better to reduce our dependency on the uptime of harbor/artifactory.
            cluster_config_rancher_kubernetes_engine_config_services_kube_api_always_pull_images=dict(type='bool', default=False),
            cluster_config_rancher_kubernetes_engine_config_services_kube_api_audit_log_enabled=dict(type='bool', default=True),
            cluster_config_rancher_kubernetes_engine_config_services_kube_api_event_rate_limit_enabled=dict(type='bool', default=True),
            cluster_config_rancher_kubernetes_engine_config_services_kube_api_pod_security_policy= dict(type='bool', default=True),
            cluster_config_rancher_kubernetes_engine_config_services_kube_api_secrets_encryption_config_enabled=dict(type='bool', default=True),
            cluster_config_rancher_kubernetes_engine_config_services_kube_api_service_node_port_range=dict(type='str', required=True),
            cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_anonymous_auth=dict(type='bool', default=False),
            cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_protect_kernel_defaults=dict(type='bool', default=True),
            cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_make_iptables_util_chains=dict(type='bool', default=True),
            cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_streaming_connection_idle_timeout=dict(type='str', default="1800s"),
            cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_tls_cipher_suites=dict(type='str', default=self.tls_cipher_suite_string),
            cluster_config_rancher_kubernetes_engine_config_services_scheduler_extra_args_address=dict(type='str', default="127.0.0.1"),
            cluster_config_rancher_kubernetes_engine_config_services_scheduler_extra_args_profiling=dict(type='bool', default=False),
            cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_address=dict(type='str', default="127.0.0.1"),
            cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_profiling=dict(type='bool', default=False),
            cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_terminated_pod_gc_threshold=dict(type='str', default="1000"),
            cluster_config_rancher_kubernetes_engine_config_ssh_agent_auth=dict(type='bool', default=False),
            cluster_config_windows_prefered_cluster=dict(type='bool', default=False),
            cluster_template_id=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=True),
            rancher_domain=dict(type='str', required=True),
            vcenter_datacenter=dict(type='str', required=False),
            vcenter_default_datastore=dict(type='str', required=False),
            vcenter_domain=dict(type='str', required=False),
            vcenter_folder=dict(type='str', required=False),
            vcenter_password=dict(type='str', required=False, no_log=True),
            vcenter_tls_insecure=dict(type='bool', required=False, default=False),
            vcenter_username=dict(type='str', required=False),
            version_name=dict(type='str', required=True),
        )

        # Module input variables
        self.api_bearer_token = None
        self.rancher_domain = None
        self.cluster_config_default_cluster_role_for_project_members = None
        self.cluster_config_default_pod_security_policy_template_id = None
        self.cluster_config_docker_root_dir = None
        self.cluster_config_enable_cluster_alerting = None
        self.cluster_config_enable_cluster_monitoring = None
        self.cluster_config_enable_network_policy = None
        self.cluster_config_local_cluster_auth_endpoint_enabled = None
        self.cluster_config_rancher_kubernetes_engine_config_addon_job_timeout = None
        self.cluster_config_rancher_kubernetes_engine_config_authentication_strategy = None
        self.cluster_config_rancher_kubernetes_engine_config_cloud_provider_name = None
        self.cluster_config_rancher_kubernetes_engine_config_custom_addons = None
        self.cluster_config_rancher_kubernetes_engine_config_ignore_docker_version = None
        self.cluster_config_rancher_kubernetes_engine_config_ingress_provider = None
        self.cluster_config_rancher_kubernetes_engine_config_ingress_extra_args = None
        self.cluster_config_rancher_kubernetes_engine_config_ingress_options = None
        self.cluster_config_rancher_kubernetes_engine_config_kubernetes_version = None
        self.cluster_config_rancher_kubernetes_engine_config_monitoring_provider = None
        self.cluster_config_rancher_kubernetes_engine_config_network_mtu = None
        self.cluster_config_rancher_kubernetes_engine_config_network_options_flannel_backend_type = None
        self.cluster_config_rancher_kubernetes_engine_config_network_plugin = None
        self.cluster_config_rancher_kubernetes_engine_config_private_registries = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_enabled = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_intervalHours = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_retention = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_safe_timestamp = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_creation = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_extra_args_election_timeout = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_extra_args_heartbeat_interval = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_gid = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_retention = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_snapshot = None
        self.cluster_config_rancher_kubernetes_engine_config_services_etcd_uid = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_always_pull_images = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_audit_log_enabled = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_event_rate_limit_enabled = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_pod_security_policy = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_secrets_encryption_config_enabled = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_service_node_port_range = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_address = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_profiling = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_terminated_pod_gc_threshold = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_anonymous_auth = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_protect_kernel_defaults = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_make_iptables_util_chains = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_streaming_connection_idle_timeout = None
        self.cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_tls_cipher_suites = None
        self.cluster_config_rancher_kubernetes_engine_config_services_scheduler_extra_args_address = None
        self.cluster_config_rancher_kubernetes_engine_config_services_scheduler_extra_args_profiling = None
        self.cluster_config_rancher_kubernetes_engine_config_ssh_agent_auth = None
        self.cluster_config_windows_prefered_cluster = None
        self.cluster_template_id = None
        self.enabled = None
        self.vcenter_default_datastore = None
        self.vcenter_datacenter = None
        self.vcenter_domain = None
        self.vcenter_folder = None
        self.vcenter_password = None
        self.vcenter_tls_insecure = None
        self.vcenter_username = None
        self.version_name = None

        # Internal variables that aren't set through the module input
        self.path = '/v3/clusterTemplateRevisions'

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

        rke_revision_id = self.revision_exists()

        if rke_revision_id is False:
            self.create_rke_revision()
        else:
            self.results['rke_revision_id'] = rke_revision_id

        return self.results

    def create_rke_revision(self):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'POST'

        data = {
            "clusterConfig": {
                "defaultClusterRoleForProjectMembers": self.cluster_config_default_cluster_role_for_project_members,
                "defaultPodSecurityPolicyTemplateId": self.cluster_config_default_pod_security_policy_template_id,
                "dockerRootDir": self.cluster_config_docker_root_dir,
                "enableClusterAlerting": self.cluster_config_enable_cluster_alerting,
                "enableClusterMonitoring": self.cluster_config_enable_cluster_monitoring,
                "enableNetworkPolicy": self.cluster_config_enable_network_policy,
                "localClusterAuthEndpoint": {
                    "enabled": self.cluster_config_local_cluster_auth_endpoint_enabled,
                    "type": '/v3/schemas/localClusterAuthEndpoint'
                },
                "rancherKubernetesEngineConfig": {
                    "addonJobTimeout": self.cluster_config_rancher_kubernetes_engine_config_addon_job_timeout,
                    # Default addons from https://rancher.com/docs/rancher/v2.x/en/security/hardening-2.4/ without the rancher
                    # ingress as we ship our own and without tiller as we only use helm v3
                    "addons": self.cluster_config_rancher_kubernetes_engine_config_custom_addons + '\n' + '''---
apiVersion: v1
kind: Namespace
metadata:
  name: cattle-system
---
apiVersion: v1
kind: Namespace
metadata:
  name: ingress-nginx
  labels:
    ingress: "true"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
name: default-psp-role
namespace: cattle-system
rules:
- apiGroups:
  - extensions
  resourceNames:
  - default-psp
  resources:
  - podsecuritypolicies
  verbs:
  - use
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: default-psp-rolebinding
  namespace: cattle-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: default-psp-role
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:serviceaccounts
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:authenticated
---
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  requiredDropCapabilities:
  - NET_RAW
  privileged: false
  allowPrivilegeEscalation: false
  defaultAllowPrivilegeEscalation: false
  fsGroup:
    rule: RunAsAny
  runAsUser:
    rule: MustRunAsNonRoot
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  volumes:
  - emptyDir
  - secret
  - persistentVolumeClaim
  - downwardAPI
  - configMap
  - projected
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: psp:restricted
rules:
- apiGroups:
  - extensions
  resourceNames:
  - restricted
  resources:
  - podsecuritypolicies
  verbs:
  - use
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: psp:restricted
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: psp:restricted
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:serviceaccounts
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:authenticated''',
                    "authentication": {
                        "strategy": self.cluster_config_rancher_kubernetes_engine_config_authentication_strategy,
                        "type": '/v3/schemas/authnConfig'
                    },
                    "ignoreDockerVersion": self.cluster_config_rancher_kubernetes_engine_config_ignore_docker_version,
                    "ingress": {
                        "provider": self.cluster_config_rancher_kubernetes_engine_config_ingress_provider,
                        "options": self.cluster_config_rancher_kubernetes_engine_config_ingress_options,
                        "extraArgs": self.cluster_config_rancher_kubernetes_engine_config_ingress_extra_args,
                        "type": '/v3/schemas/ingressConfig'
                    },
                    "kubernetesVersion": self.cluster_config_rancher_kubernetes_engine_config_kubernetes_version,
                    "monitoring": {
                        "provider": self.cluster_config_rancher_kubernetes_engine_config_monitoring_provider,
                        "type": '/v3/schemas/monitoringConfig'
                    },
                    "network": {
                        "mtu": self.cluster_config_rancher_kubernetes_engine_config_network_mtu,
                        "options": {
                            "flannel_backend_type": self.cluster_config_rancher_kubernetes_engine_config_network_options_flannel_backend_type
                        },
                        "plugin": self.cluster_config_rancher_kubernetes_engine_config_network_plugin,
                        "type": '/v3/schemas/networkConfig'
                    },
                    "services": {
                        "etcd": {
                            "backupConfig": {
                                "enabled": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_enabled,
                                "intervalHours": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_intervalHours,
                                "retention": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_retention,
                                "safeTimestamp": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_safe_timestamp,
                                "type": '/v3/schemas/backupConfig'
                            },
                            "creation": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_creation,
                            "extraArgs": {
                                "election-timeout": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_extra_args_election_timeout,
                                "heartbeat-interval": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_extra_args_heartbeat_interval
                            },
                            "gid": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_gid,
                            "retention": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_retention,
                            "snapshot": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_snapshot,
                            "type": '/v3/schemas/etcdService',
                            "uid": self.cluster_config_rancher_kubernetes_engine_config_services_etcd_uid
                        },
                        "kubeApi": {
                            "alwaysPullImages": self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_always_pull_images,
                            "auditLog": {
                                "enabled": self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_audit_log_enabled,
                            },
                            "eventRateLimit": {
                                "enabled": self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_event_rate_limit_enabled,
                            },
                            "podSecurityPolicy": self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_pod_security_policy,
                            "secretsEncryptionConfig": {
                                "enabled": self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_secrets_encryption_config_enabled,
                            },
                            "serviceNodePortRange": self.cluster_config_rancher_kubernetes_engine_config_services_kube_api_service_node_port_range,
                            "type": '/v3/schemas/kubeAPIService'
                        },
                        "kubelet": {
                            "extraArgs": {
                                # Whilst we self-sign certificates we leave this hardcoded. In the future if we CA sign the cluster
                                # then this will need to be conditional
                                "feature-gates": "RotateKubeletServerCertificate=true",
                                "anonymous-auth": self.cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_anonymous_auth,
                                "protect-kernel-defaults": self.cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_protect_kernel_defaults,
                                "make-iptables-util-chains": self.cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_make_iptables_util_chains,
                                "streaming-connection-idle-timeout": self.cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_streaming_connection_idle_timeout,
                                "tls-cipher-suites": self.cluster_config_rancher_kubernetes_engine_config_services_kubelet_extra_args_tls_cipher_suites,
                            },
                            "generateServingCertificate": True,
                        },
                        "scheduler": {
                            "extraArgs": {
                                "address": self.cluster_config_rancher_kubernetes_engine_config_services_scheduler_extra_args_address,
                                "profiling": self.cluster_config_rancher_kubernetes_engine_config_services_scheduler_extra_args_profiling,
                            },
                        },
                        "kubeController": {
                            "extraArgs": {
                                "address": self.cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_address,
                                # Whilst we self-sign certificates we leave this hardcoded. In the future if we CA sign the cluster
                                # then this will need to be conditional
                                "feature-gates": "RotateKubeletServerCertificate=true",
                                "profiling": self.cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_profiling,
                                "terminated-pod-gc-threshold": self.cluster_config_rancher_kubernetes_engine_config_services_kube_controller_extra_args_terminated_pod_gc_threshold,
                            },
                        },
                        "type": '/v3/schemas/rkeConfigServices'
                    },
                    "sshAgentAuth": self.cluster_config_rancher_kubernetes_engine_config_ssh_agent_auth,
                    "type": '/v3/schemas/rancherKubernetesEngineConfig'
                },
                "type": '/v3/schemas/clusterSpecBase',
                "windowsPreferedCluster": self.cluster_config_windows_prefered_cluster
            },
            "clusterTemplateId": self.cluster_template_id,
            "enabled": self.enabled,
            "name": self.version_name,
        }

        if self.cluster_config_rancher_kubernetes_engine_config_cloud_provider_name == 'aws':
            data['clusterConfig']['rancherKubernetesEngineConfig']['cloudProvider'] = {
                "awsCloudProvider": {
                    "type": '/v3/schemas/awsCloudProvider'
                },
                "name": self.cluster_config_rancher_kubernetes_engine_config_cloud_provider_name,
                "type": '/v3/schemas/cloudProvider'
            }

        if self.cluster_config_rancher_kubernetes_engine_config_cloud_provider_name == 'vsphere':
            data['clusterConfig']['rancherKubernetesEngineConfig']['cloudProvider'] = {
                "vsphereCloudProvider": {
                    "type": '/v3/schemas/vsphereCloudProvider',
                    "global": {
                        "type": '/v3/schemas/globalVsphereOpts',
                        "insecure-flag": self.vcenter_tls_insecure,
                        "soap-roundtrip-count": 0
                    },
                    "virtualCenter": {
                        self.vcenter_domain: {
                            "type": '/v3/schemas/virtualCenterConfig',
                            "datacenters": self.vcenter_datacenter,
                            "user": self.vcenter_username,
                            "password": self.vcenter_password,
                        }
                    },
                    "workspace": {
                        "datacenter": self.vcenter_datacenter,
                        "server": self.vcenter_domain,
                        "folder": self.vcenter_folder,
                        "default-datastore": self.vcenter_default_datastore,
                    },
                },
                "name": self.cluster_config_rancher_kubernetes_engine_config_cloud_provider_name,
                "type": '/v3/schemas/cloudProvider'
            }

        if self.cluster_config_rancher_kubernetes_engine_config_private_registries:
            for registry in self.cluster_config_rancher_kubernetes_engine_config_private_registries:
                if list(registry.keys()).sort() != [ 'isDefault', 'url', 'user' ].sort():
                    self.module.fail_json(msg='RKE Template Create request unsuccessful. Private registry config requires "url", "isDefault" and "user" to be set. Got: ' % registry)
                else:
                    registry["type"] = '/v3/schemas/privateRegistry'
            
            data['clusterConfig']['rancherKubernetesEngineConfig']["privateRegistries"] = [
                registry for registry in self.cluster_config_rancher_kubernetes_engine_config_private_registries
            ]

        resp, info = fetch_url(self.module, self.rancher_domain + self.path, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 201:
            print(data, headers, request_type)
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' creating an RKE template'

            self.module.fail_json(msg='RKE Template Create request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())

        self.results['changed'] = True
        self.results['rke_revision_id'] = decoded_response['id']

    def revision_exists(self):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        query = {
            'name': self.version_name,
            'clusterTemplateId': self.cluster_template_id,
        }

        request_type = 'GET'
        url = self.path + '?' + urlencode(query)
        resp, info = fetch_url(self.module, self.rancher_domain + url, headers=headers, method=request_type)

        if info["status"] != 200:
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' listing existing template versions'

            self.module.fail_json(msg='RKE Template List request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())
        items = len(decoded_response['data'])

        # TODO: Check if there are other numbers of items returned and handle appropriately
        if items == 1:
            return decoded_response['data'][0]['id']

        return False

def main():
    RancherRKETemplateVersion()

if __name__ == '__main__':
    main()