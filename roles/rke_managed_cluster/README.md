# Rancher Cluster Creation Parameters  
There are five steps in creating a cluster, each of which has a sets of parameters. Defaults have been provided for all parameters in the defaults/main.yml. The parmameters are required by the Python scripts used in each of the six steps of cluster creation:

1. Creating a new cluster Definition
1. Create RKE template Object
1. Create RKE template Version
1. Create Node Template
1. Create Cluster
1. Add Nodepools To Cluster

To ensure each parameter within the Python script has a unique name, its JSON path is container within its name and is preceeded with 'rke_'

## Creating a new cluster Definition
The creation of a new cluster only requires you to specify the parameters that are different for that cluster in a new playbook. For example:  

- hosts: type_bastion  
  remote_user: centos  
  roles:  
    - rancher_configuration  
    - role: rke-managed-cluster  
      rke_control_plane_nodepool_prefix: ops-cp-  
      rke_etcd_nodepool_prefix: ops-etcd-  
      rke_worker_nodepool_prefix: ops-wp-  
      rke_cluster_tag: ops  
      rke_node_template_name: CIS Hardened Centos 7 AMI - Ansible Managed (Ops Cluster)  
      rke_cluster_name: ops-cluster  
      rke_cluster_config_rancher_kubernetes_engine_config_kubernetes_version: "{{ ops_cluster_kubernetes_version }}"  

## Create RKE template Object
Library file that uses the parameters: rancher_create_rke_template_version.py
Description: This step creates a object that will hold sets of parameters common to one or more clusters. It is the first step in cluster creation.

Required parameters:
* rke_managed_cluster_rancher_domain: < The FQDN of the cluster being created. e.g. dsab.example.com >
* rke_api_bearer_token: < The token username and password concatenated together > See: https://rancher.com/docs/rancher/v2.x/en/user-settings/api-keys/
* rke_node_template_name: "< The name of the node template to create/update >"
* rke_validate_certs: False

## Create RKE template Version
Library file that uses the parameters: rancher_create_rke_template_version.py
Description: This step adds common cluster parameters to a "RKE template". The template is specified when creating a cluster to set the parameters. It is the second step in cluster creation.

Required parameters:  
* rke_cluster_config_default_cluster_role_for_project_members: < The default cluster role users need membership of to access the cluster, or null >  
* rke_cluster_config_enable_cluster_alerting: < Should always be set to false >  
* rke_cluster_config_enable_cluster_monitoring: < Whether to enable cluster monitoring, e.g. true/false >  
* rke_cluster_config_enable_network_policy: < Whether to place restrictions on container communication, e.g. true/false >  
* rke_cluster_config_local_cluster_auth_endpoint_enabled: < Whether to enable a cluster endpoint to allow direct access to downstream clusters without authenticating through the Rancher server, for example using the kubectl command >  
* rke_cluster_config_rancher_kubernetes_engine_config_addon_job_timeout: < The time to wait for kubernetes add-on jobs to complete, e.g. a job to add a particular network plugin. >  
* rke_cluster_config_rancher_kubernetes_engine_config_authentication_strategy: < Authentication strategy to use, e.g. x509 >  
* rke_cluster_config_rancher_kubernetes_engine_config_cloud_provider_name: < The name of the cloud prodividor: e.g. aws, vsphere, etc >  
* rke_cluster_config_rancher_kubernetes_engine_config_ignore_docker_version: < Whether to allow interaction with any docker version >  
* rke_cluster_config_rancher_kubernetes_engine_config_ingress_provider: < The default ingress provider, e..g. nginx >  
* rke_cluster_config_rancher_kubernetes_engine_config_kubernetes_version: < The Kubernetes version to use, e.g. 1.17.x >  
* rke_cluster_config_rancher_kubernetes_engine_config_monitoring_provider: metrics-server  
* rke_cluster_config_rancher_kubernetes_engine_config_network_options_flannel_backend_type: < The virtual network type to use, e.g. vxlan >  
* rke_cluster_config_rancher_kubernetes_engine_config_network_plugin: < The container network interface to use, e.g. canal >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_enabled: < Whether etcd periodic backups are enabled - true/false >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_intervalHours: < The period between etcd backups, e.g. 12h >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_retention: < The retention period of etcd backups, e.g. 72h >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_kube_api_always_pull_images: < Whether to pull container images or use cached images, e.g. false >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_etcd_backup_config_safe_timestamp: < Whether to replace special characters in the snapshot filename timestamp - true/false >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_etcd_extra_args_heartbeat_interval: < Set the heartbeat interval between etcd nodes >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_etcd_gid: < The group ID of the etcd service, default 0 >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_etcd_retention: < Whether to retain etcd snapshots, e.g. true >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_etcd_snapshot: < Whether to perform periodic etcd snapshots, e.g. false >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_etcd_uid: < The group UID of the etcd service, default 0 >  
* rke_cluster_config_rancher_kubernetes_engine_config_services_kube_api_service_node_port_range: < The port range to use for pods, e.g. 30000-32767 >  
* rke_cluster_template_id: < The ID of the cluster template created in the previous step. IS THE RETURNED AUTOMATICALLY?, e.g. cattle-global-data:ct-qnznw >  
* rke_enabled: < Whether the template is enabled, e.g. True/False >  
* rke_template_name: < RKE template name >  
* rke_template_version: < RKE Template version >  

## Create Node Template
Library file that uses the parameters: rancher_ec2_node_template.py
Description: This step adds cluster specific parameters to a node template. The template is used in conjunction with an RKE template specify the unique parameter set required by the cluster. It is the third step in cluster creation.

Required parameters:  
* rke_ami_id: < The name of the ami the node template should create instances from >  
* rke_block_duration_minutes: < Specifies the number of hours spot instances should run >  
* rke_cloud_credential_id: 'cattle-global-data:cc-j25wl'  
* rke_cluster_tag: < The cluster name/type to tag all the cluster members with. Useful for billing purposes >  
* rke_device_name: < The device name of the disk, e.g. "/dev/sda1" >  
* rke_insecure_registries: [ "harbor.cloudranger.co.uk:80" ]  
* rke_ec2_size: < The size of the ec2 instances that should be created >  
* rke_encrypt_ebs_volumes: < Whether to encrypt the EBS volumes attached to the AWS nodes - True/False >  
* rke_endpoint: < Optional endpoint URL (hostname only or fully qualified URI) (string) >  
* rke_engine_install_url: < The URL of the script that install docker. e.g. https://harbor.rancher.co.uk/library/install-docker/19.03.sh >  
* rke_insecure_transport: < Disables SSL when sending requests - True/False >  
* rke_iam_instance_profile: < The IAM profile name used to authenticate with, usually RKECloudProvisioner >  
* rke_keypair_name: < The optional name assigned to the keypair being used to launch the EC2 instances >  
* rke_monitoring: < Whether to monitor, collect, and analyse instance metrics through Amazon CloudWatch. - True/False >  
* rke_node_template_name: "CIS Hardened Centos 7 AMI - Ansible Managed"  
* rke_private_address_only: < Whether to restrict the cluster inter-node communications to the private IPs only - True/False >  
* rke_region_zone: < The region within the AWS zone in which to launch the cluster nodes >  
* rke_request_spot_instance: < Whether to request AWS spot instances for the cluster nodes - True/False >  
* rke_retries: < The number of retries of HTTP requests to AWS services >  
* rke_root_size: < The size of the root disk in GB to use. It must match the root disk size if the ami specified in the rke_ami_id parameter, e.g. 80 >  
* rke_region: < The region to deploy the ec2 instances into >  
* rke_schedule_tag: < Used to specify the name of a tag that controls the nodes start-up/shutdown times (if required). Usually uk-office-hours >  
* rke_security_group: < The AWS security group name to assign to the instance >  
* rke_security_group_readonly: < Whether or not the security group should be set to read only - True/False >	  
* rke_session_token: < The optional temporary session token to use for calls to the AWS SDK >  
* rke_spot_price: < AWS spot instance bid price (in dollar), e.g. "0.50" >  
* rke_subnet_id: < The name of the subnet the node template should create instances in (needs to be in the vpc specified in the rke_vpc_id param) >  
* rke_ssh_user: < The ssh user that should be used to log into the AMI >  
* rke_use_ebs_optimized_instances: < whether to create an EBS optimized instance - True/False >  
* rke_use_internal_ip_address: < Whether the internal ports between EC2 instances are open to each other - True/False >  
* rke_use_private_address: < Whether to force the use of only the private address - True/False >  
* rke_userdata: < Specify user data to configure an instance or run a configuration script during launch >  
* rke_validate_certs: < Whether to validate any certificates used - True/False >  
* rke_volume_type: < Specify the type of volume to use - gp2 (general purpose), io1 (provisioned IOPs) or Standard (Magnetic) >  
* rke_vpc_id: < The name of the VPC the node template should create instances in >  
  
## Create Cluster  
Library file that uses the parameters: rancher_cluster.py  
Description: This step creates a cluster object with the parameters provided by the RKE and node templates. It is the fourth step in cluster creation.

Required parameters:
* rke_cluster_name: < The name of the cluster to display on Rancher >

## Add Nodepools To Cluster
Library file that uses the parameters: rancher_manage_nodepool.py
Description: This final step creates three pools of nodes - controller, etcd & worker - and adds them to the cluster object created in the previous step. The result should be a fully working cluster with nodes of each type.

Required parameters:  
* rke_control_plane: < whether to create a control plane nodepool, - true/false >  
* rke_control_plane_quantity: < The number of pool members, usually 2 for redundancy >  
* rke_control_plane_nodepool_prefix: < The node prefix to use for each node member, e.g. "dasb-cntl" >  
* rke_etcd: < whether to create an etcd nodepool, - true/false >  
* rke_etcd_quantity: < The number of etcd pool members. Must be an odd number, usually 3, to ensure a quorum is achieved. >  
* rke_etcd_nodepool_prefix: < The node prefix to use for each node member, e.g. "dasb-etcd" >  
* rke_worker: < whether to create a worker nodepool, - true/false   
* rke_worker_quantity: < The number of worker nodes to start the cluster with, minimum 1 >  
* rke_worker_nodepool_prefix: < The node prefix to use for each node member, e.g. "dasb-wrkr" >  
* rke_delete_not_ready_after_secs: < The number of seconds to wait for a node to join before it is removed and rebuilt >  
* rke_type: nodePool  
