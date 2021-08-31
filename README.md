# Ansible Platform Configuration

## Set-up the build server
The following steps are required to set-up the build server with the necessary software:

### Install Ansible - OLD
```
$ sudo apt install -y python3 python3-pip
$ sudo apt install software-properties-common
$ sudo apt-add-repository ppa:ansible/ansible -y
$ sudo apt update
$ sudo apt install ansible -y
$ ansible --version
$ pip3 install --upgrade pip setuptools
$ pip3 install pyvmomi jmespath
```

Note: Had to execute this to resolve an existing plugin that thought it was missing:
```
ansible-galaxy collection install community.docker
```

### Install Ansible - New
Use the following command to install all the applications required to build the platform:

```
$ sudo apt install -y python3 python3-pip
$ pip3 install -r requirements.txt
```

For local install, it may be preferable to use a virtual envirinment:

```
$ sudo apt install python-virtualenv virtualenvwrapper
$ mkvirtualenv -p /usr/bin/python3 <environment name>
$ pip3 install requirements.txt
```

### VSphere Automation SDK
```
$ pip3 install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git
$ cat << EOF >> ~/.bashrc
# vSphere connection parameters
export GOVC_URL=rnvcentre.lab.int
export GOVC_USERNAME=administrator@rnvsphere.local
export GOVC_PASSWORD=Password123456!
export GOVC_INSECURE=true
EOF
$ . ~/.bashrc
```

### Helm for RKE & Harbour HA installation
```
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
$ chmod 700 get_helm.sh
$ ./get_helm.sh
```

### Optionally make pip3 available as pip
```
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
```

### Docker
Docker is required to be able to run the rancher-save-images.sh script that pulls the container images required to stand-up the Rancher management cluster.

```
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs)  stable"
sudo apt-get update
apt-cache madison docker-ce # List available docker versions if not installing the latest.
sudo apt-get install docker-ce -y
```

## Overview

The Rancher NAP Platform is made up of the following VMs:

* Three RKE nodes to support a Rancher cluster
* Three Postgres nodes configure as a HA database cluster with Patroni, Consul, HAProxy and Keepalived
* Three Harbor nodes configured as a HA container repository with Redis and Keepalived
* Three Hashicorp Vault nodes configured as a HA Vault cluster to hold platform and container secrets
* A single Bastion  node that provides access to all other nodes

This repository holds the Ansible code that will be run on a build server to configure all platform nodes on a vSphere/vCenter cluster. The terraform from the tf-vsphere-vm-deploy repository must have been run successfuly and created and started all platform nodes.

## Playbooks

### Initial Management

This playbook performs the initial provisioning of the nodes that make-up the management cluster - Bastion , RKE, Harbor and Postgres.

### Assemble Helm

This playbook downloads the Helm charts required to configure the Rancher cluster and needs to be run on a machine with internet access. The Helm charts produced are required by the final_management.yml playbook.

### Final Management

This playbook requires docker images used by for the Rancher cluster to have been loaded into Harbor and the Helm packages placed in the ubuntu user's home directory on the Bastion  server.

## Inventory tags used by Ansible

The Ansible code determines the appropriate playbook to run against each node by reading the vSphere tags have been assigned by Terraform. The tags are as follows:

- *env* The environment (e.g. env_dev, env_preprod, env_prod)
- *cluster* The K8s cluster type (currently supported values: cluster_rke, cluster_applications)
- *cluster_member* The K8s cluster member type (currently supported values: cluster_control_member, cluster_etcd_member, cluster_etcd_member)
- *type* The software type installed on the node (currently supported values: rke, Bastion , vault, harbor, redis, postgres_ha, helm)

All VMs are allocated a single environment tag and one or more software type tags. All clusters members are allocated a cluster member tag.

SSH key-pair based access from the build server will have already been configured by Terraform, so Ansible will have the access it requires to each node.

## Active Directory Structure

*** TBC ***

## Steps to deploy

Helm needs to be installed on an internet facing machine is order to retrieve the Helm charts required to install Rancher. Install via the machines package manager or using the following steps:

$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
$ chmod 700 get_helm.sh
$ ./get_helm.sh

[See](https://helm.sh/docs/intro/install/) for futher information.

### Certificates

*If on an environment is using custom SSL Certificates*, create them by following the process found at https://jamielinux.com/docs/openssl-certificate-authority/sign-server-and-client-certificates.html. They will be copied to the Bastion server automatically during the execution of the final_management.yml playbook. By default, the certificates need to be present on the build server in the /var/tmp/rancher_certs directory and with the following structure (the certificate names can be changed in the environments environment.yml file)

    /var/tmp/rancher_certs
    ├── certs
    │   ├── # Trusted root certs....
    ├── harbor.lab.int.cert.full.chain.pem
    ├── harbor.lab.int.cert.pem
    ├── intermediate
    │   ├── certs
    │   │   └── rancher-intermediate.cert.pem
    │   └── private
    │       └── rancher-intermediate.key.pem
    ├── rancher-ca.cert.pem
    ├── rancher-ca-chain.cert.pem
    ├── openssl.cnf
    └── private
        ├── harbor.lab.int.key.pem
        └── rancher-ca.key.pem

### Run the provision_management.yml playbook

Note: Make sure the build server has no entries in /home/ubuntu/.ssh/known_hosts for the postgres, redis and harbor VIPs

1. From the build server, run the Initial Management playbook:

`ansible-playbook -u ubuntu -i inventory/dev/dev.vmware.yaml provision_management.yml --skip-tags online_install,keepalived-install`

### Check / Configure Harbor's AD Authentication (if required)

1. Confirm Harbor has been set-up with Active Directory (AD) authentication

NOTE: Because the users are managed by AD, self-registration, creating users, deleting users, changing passwords, and resetting passwords must be performed in AD.
      DO NOT add any local user accounts to Harbor. AD users should be made a member of the AD group specified in the LDAP settings below.

Ansible will have configured the AD parameters. Here is an example of what they could be:
    1. Log into harbor with the "admin" / "Password123456" credentials.
    1. Check the LDAP (Active Directory) parameters are correct to allow the system to authenticate users.
        LDAP URL:                       ldap://192.168.142.2
        LDAP Search DN:                 CN=SA-RN-HARBOR,OU=Service_Accounts,OU=rancher,DC=ibm,DC=lab,DC=int
        LDAP Search Password:           Password123456
        LDAP Base DN:                   OU=Users,OU=Rancher,DC=ibm,DC=lab,DC=int
        LDAP Filter:                    objectClass=person
        LDAP UID:                       sAMAccountName
        LDAP Scope:                     Subtree
        LDAP Group Base DN:             CN=rancher-harbor-admins,OU=Groups,OU=Rancher,DC=ibm,DC=lab,DC=int  # NOTE: Due to bug https://github.com/goharbor/harbor/issues/13156, this must be the same as the LDAP Group Admin DN
        LDAP Group Filter:              objectClass=group
        LDAP Group GID:                 cn
        LDAP Group Admin DN:            CN=rancher-harbor-admins,OU=Groups,OU=Rancher,DC=ibm,DC=lab,DC=int
        LDAP Group Membership:          memberof
        LDAP Scope:                     Subtree
    1. Click the TEST LDAP SERVER button to confirm Harbor can access the AD service.
    1. Under Administration/Groups, add a new group called 'harbor_admins' with the same DN as the LDAP admin group, i.e. CN=rancher-harbor-admins,OU=Groups,OU=Rancher,DC=ibm,DC=lab,DC=int. Members of the rancher-harbor-admins AD group will now have access to Harbor.
    1. If desired, in 'Users & Groups' on a Windows AD server, add a user to the AD group configured in the LDAP settings for the Harbor administrators - 'rancher-harbor-admins' in the example above.
    1. In the Harbor web UI, add a project called 'rancher'.
    1. In Harbor web UI, select Projects/rancher/Members. Clicking '+ GROUP' button and select the 'harbor_admins' group from the Add Group Member window.
    1. Login to the Harbor web UI as an AD member of the Admin group and check the account can access the rancher project and view the repositories tab (empty at this stage).

### Rancher Container Images

[See] https://github.com/rancher/rancher/releases/tag/v2.5.5

1. Run the following steps from a server that has docker installed and has internet connectivity to download the container images required to build the Rancher cluster on the RKE nodes.

    1. mkdir ~/rancher_install_files && cd ~/rancher_install_files
    1. wget https://github.com/rancher/rancher/releases/download/v2.5.5/rancher-images.txt
    1. wget https://github.com/rancher/rancher/releases/download/v2.5.5/rancher-save-images.sh
    1. wget https://github.com/rancher/rancher/releases/download/v2.5.5/rancher-load-images.sh
    1. chmod +x rancher-*-images.sh

    [NOTE] Before proceeding, check that the /var/lib/docker folder contains multiple directories. If not, restart the docker service and check again.

    1. Download the containers from Rancher by executing ./rancher-save-images.sh
    1. Transfer the rancher_install_files directory to the ubuntu user's home directory on the Bastion server: 'scp -rp ~/rancher_install_files/ ubuntu@<Bastion  IP>:'
    1. On the Bastion server, login as the ubuntu user and move the rancher_install_files to the /var/lib/docker directory: 'sudo mv ~/rancher_install_files/ /var/lib/docker/'
    1. Make sure the system_rancher has read/write access to the /var/lib/docker/rancher_install_files directory: 'sudo chown -R root:system_rancher /var/lib/docker/rancher_install_files/'
    1. Switch to the system_rancher user: 'sudo -iu system_rancher' and 'cd /var/lib/docker/rancher_install_files'
    1. Execute 'docker login -u system_rancher -p <password> <Harbor repo FQDN>'.
    e.g. docker login -u system_rancher harbor.lab.int[<:port>] # Password should be prompted for. You may not be able to pass it on the command line depending on the repo s/w. E.G. You can't with Nexus.
    1. Execute './rancher-load-images.sh -i rancher-images.tar.gz -r <Harbor rerp FQDN>/rancher | tee ~/harbor_load.log'

    This will load the containers into the Bastion  node's docker cache and then push them to the Harbor container repository. There are 161 images for rancher version 2.5.5. This will take a long time and requires over 41GB of free disk space in /var/lib/docker. The command will return nothing until it has extratced the images from the rancher-images.tar.gz file and begun loading them into the cache. Progress of the cache load can be monitored by executing: ssh -t ubuntu@<Bastion  IP> watch 'df -k /var/lib/docker' from another terminal window. Once the full process is complete there should be 115 individual repositories listed in the 'rancher' project on the Harbor server, (with some holding multiple versions) containing a total of 161 images.

   [NOTE]: If any files fail the push to Harbor, these can be identied in the terminal session log by greping it for "unauthorized". Tag and push these images manually as system_rancher. The following example tags and pushes the rancher/webhook-receiver container image:

```
    system_rancher@bastion: docker images | grep webhook-receiver
    rancher/webhook-receiver                                                 v0.2.4                         579c7a5cd510   6 months ago    18.9MB

    system_rancher@bastion: docker tag rancher/webhook-receiver:v0.2.4 <Harbor repo FQDN>/rancher/rancher/webhook-receiver:v0.2.4
    system_rancher@bastion: docker push <Harbor repo FQDN>/rancher/rancher/webhook-receiver:v0.2.4
```

### Additional cert-manager v0.8.1 container images (if using cert-manager to manage certs))

The Rancher container images for v2.5.5 include cert-manager v0.8.1. Additional images need to be pulled from Redhat's https://quay.io site and pushed up to our Harbor repository. A free account is required to be able to access the https://quay.io site. Follow the steps below from a machine with internet access:

    1. On a machine with docker installed and with internet access, set-up a free account by accessing https://quay.io/repository
    1. From a user with docker access, login to the repository using the account and password created in step 1.
    
    ```
    $ docker login -u <user> -p <password> quay.io
    ```

    Pull the updated container images:

    ```
    $ docker pull quay.io/jetstack/cert-manager-webhook:v0.8.1
    $ docker pull quay.io/jetstack/cert-manager-cainjector:v0.8.1
    $ docker pull quay.io/jetstack/cert-manager-controller:v0.8.1
    ```
    
    Tag the images for the Rancher Harbor repository and push them to it:

    ```
    $ docker tag quay.io/jetstack/cert-manager-webhook:v0.8.1 harbor.lab.int/rancher/quay.io/jetstack/cert-manager-webhook:v0.8.1
    $ docker tag quay.io/jetstack/cert-manager-cainjector:v0.8.1 harbor.lab.int/rancher/quay.io/jetstack/cert-manager-cainjector:v0.8.1
    $ docker tag quay.io/jetstack/cert-manager-controller:v0.8.1 harbor.lab.int/rancher/quay.io/jetstack/cert-manager-controller:v0.8.1
    ```

    Login to the Harbor repository and push the images:

    $ docker login -u system_rancher -p Password123456! harbor.lab.int
    $ docker push harbor.lab.int/rancher/quay.io/jetstack/cert-manager-webhook:v0.8.1
    $ docker push harbor.lab.int/rancher/quay.io/jetstack/cert-manager-cainjector:v0.8.1
    $ docker push harbor.lab.int/rancher/quay.io/jetstack/cert-manager-controller:v0.8.1
    ```

### Set-up Helm Charts - This is now automated and the helm charts added to this repo.

As the following v0.8.1 deployment.yaml charts each require their apiVersion changing from apps/v1beta1 to apps/v1, they have been modified and included in this repository along with the additional custom resource definitions. The rancher_helm_chart_transfer role is used to transfer the charts to the Bastion server, backing-up any that already exist. The source of the files can be overridden using the role's 'helm_chart_source' parameter.

The charts were originally pulled from an internet facing machine that has Ansible and Helm installed using the following steps:

1. Clone the ansible-rn repository and run: `ansible-playbook assemble_helm.yml` This generates the helm charts in the /tmp/helm-templates directory.
1. Add the cert-manager custom resource definitions:

$ curl -kL  https://raw.githubusercontent.com/jetstack/cert-manager/release-0.8/deploy/manifests/00-crds.yaml -o /tmp/helm-templates/00-crds.yaml

1. Change 'apps/v1beta1' to 'apps/v1' in the following charts:

* cert-manager/charts/cainjector/templates/deployment.yaml
* cert-manager/charts/webhook/templates/deployment.yaml
* cert-manager/templates/deployment.yaml

1. Transfer the templates to the Bastion server:
$ scp -rp /tmp/helm-templates/ ubuntu@<Bastion IP>:

### Run the Final Management Playbook

1. From the build server, run the Final Management playbook `ansible-playbook -u ubuntu -i inventory/dev/dev.vmware.yaml final_management.yml --skip-tags online_install,keepalived-install`

If you are rebuilding the RKE managed cluster then be sure to delete any existing RKE state file that may exist. These
can cause your cluster not to spin up with mysterious errors (especially if you've tried to keep the same elastic IPs!)

[NOTE] The cert_from_ca_intermediate_cert_pem param in ansible-rn/group_vars/type_env_dev/environments.yml determines the name of the CA root cert & key to use when creating the Rancher cert, e.g. rancher-intermediate.cert.pem

## Setup Rancher Managed Clusters (if required)

Once you have a functional rancher cluster and have created the cluster credentials (manually at the moment to keep secrets secret), this provisions the Rancher UI with functional clusters and AD Authentication.

To create a new cluster it is necessary to either create a new ansible playbook at the root directory of this repo, or add the clusters definition to an existing playbook. For example: 

```
test-cluster.yml:
  - hosts: type_Bastion   
  remote_user: ubuntu
  roles:  
    - role: rke-managed-cluster  
      rke_control_plane_nodepool_prefix: test-cntl  
      rke_etcd_nodepool_prefix: test-etcd  
      rke_worker_nodepool_prefix: test-wrkr  
      rke_cluster_tag: test-cluster  
      rke_node_template_name: Ubuntu-18.04-CIS-vmware-rancher-v01
      rke_cluster_name: test-cluster  
```

Run the new playbook to create the cluster:

  ansible-playbook --private-key ~/.ssh/id_rsa -i inventory/dev/dev.vmware.yml  test-cluster.yml

## Provision Managed Clusters

This provisions keepalived on an existing cluster. This playbook needs to be kept minimal and the long term intention
is that all this behavior should be delgated to cloud-init eventually so that all clusters can be completely
dynamically provisioned.

Note that the playbook accepts an argument to specify which cluster to run against. By default it runs against the apps
cluster by running like:

  ansible-playbook -i inventory/dev/rancher.vmware.yaml provision_clusters.yml

However it can also run against the ops cluster - for example:

  ansible-playbook -i inventory/dev/rancher.vmware.yaml provision_clusters.yml -e target_cluster_name=ops

As this runs against a cluster you need to have a .ssh config file setup to use the Rancher Generated SSH keys. This is
time consuming unfortunately and has scope for automation in the future. For each worker node you will need the following
in your `.ssh/config` file:

```
Host <HOSTNAME> <IP_ADDRESS>
  Hostname <IP_ADDRESS>
  IdentityFile ~/.ssh/<HOSTNAME>
  IdentitiesOnly yes
```

substituting the hostname and ip address of the vm with the rancher named file. Note these keys will obviously have to be
swapped out if the node is rebuilt. Note when running this code on Bastion  boxes (i.e. VMWare envs - as ansible is run
as sudo this config file and keys must be for the ROOT user not the centos user)

## To Install New version or roles

```
ansible-galaxy role install --roles-path ./galaxy-roles -r requirements.yml
```

## To Install New version or collections

```
ansible-galaxy collection install -p ./collections -r requirements.yml
```

You will need to add the `--force` option if you are performing an update and you already have the directory present. We choose to commit the galaxy files here (even though
technically not best pratice as it's easier to manage in the air-gapped environments and also because galaxy is just a simple proxy to github and thus if a repo is deleted
the galaxy urls with 404 leaving you stuck. By keeping them in Git we guarentee that they are available.
