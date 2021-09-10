# Downloading Helm Templates

The Ansible playbooks in this repository are used to create the helm templates and deploy the RKE cluster with Rancher. 

## Helm Set Up
SSH into the Bastion server created using Terraform in the `rancher-setup` repository. The helm installation and the rendering of the appropriate Helm charts that are required for Rancher to be installed are done by an ansible playbook. 

```
$ cd
$ git clone https://github.com/mollymcclean/scp-ansible-rn
$ cd ~/scp-ansible-rn
$ ansible-playbook assemble_helm.yml
```
The playbook will :

- Create a temporary directory for the helm templates, /tmp/helm-templates.
- Add the required helm chart repository.
- Pull down the latest Rancher chart and save it in the directory as a .tgz file.
- Render the Helm Template for the rancher chart with required options for an air-gapped environment, and the appropriate SSL option, using the Rancher container images.

Variables to edit in `group_vars/*/rancher.yml` and in `roles/rancher_helm_setup/defaults/main.yml`:
- `rancher_version: 2.5.9`
- `rancher_url: <Load Balancer DNS>`
- `rancher_docker_registry: <Registry DNS:PORT>`
- `cert_manager_version: v1.0.4`


This repository holds the Ansible code that will be run on a build server to configure all platform nodes on a vSphere/vCenter cluster. The terraform from the tf-vsphere-vm-deploy repository must have been run successfuly and created and started all platform nodes.

## Playbooks
So far, `assemble_helm.yml` is the only playbook that has been run. For future work, we hope to incorporate the `provision_management.yml` playbook.

### Management Cluster Provisioning and Rancher Installation

Test the `provision_management.yml` playbook to automate the RKE cluster creation and Rancher deployment.

In this repository, provision_management.yml combines `initial_management.yml` and `final_management.yml`. The inventory for the `provision_management.yml` playbook needs to be edited to match the secure environment. The host groups required are `type_bastion`, `type_helm` and `type_rke`.

Can directly edit the hosts file `inventory/dev/hosts.ini`, to put the Bastion IP under both `type_bastion` and `type_helm` groups (with ansible_connection=local), and all 3 RKE node IPs under `type_rke` group. All other groups should be empty.

Alternatively, the inventory host path can be set to `inventory/dev/dev.vmware.yaml`, which will search for vmware hosts in `rnvcentre.lab.int` tagged with `type_*`, and `env_dev`.

The provision_management ansible playbook should be run from the secure environment with the following command:
```
$ ansible-playbook -u ubuntu -i inventory/dev/hosts.ini provision_management.yml --limit 'type_bastion:type_rke' --skip-tags online_install,keepalived-install
```

Added to the command is the `--limit` argument, as only hosts of `type_bastion` and `type_rke` will be transferable from the RN environment for this playbook.

The `--skip-tags` argument exists because this code was adapted from code used in a non-airgapped environment, and so also includes roles/tasks that require internet access. These were tagged by RN so that the code could be maintained, while skipping over the parts that, in this secure environment, need to be done separately.

This playbook will add disks to the Bastion and RKE nodes, create certificates, transfer the Helm charts to the Bastion node, prepare the RKE nodes, provision the RKE cluster and deploy Rancher.

---
## Descriptions
The text below has been copied from the royal navy's ansible-rn repository.

https://bitbucket.org/automationlogic/ansible-rn/src/master/

### Initial Management

This playbook performs the initial provisioning of the nodes that make-up the management cluster - Bastion, RKE, Harbor and Postgres.

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


### How to run the Final Management Playbook

1. From the build server, run the Final Management playbook `ansible-playbook -u ubuntu -i inventory/dev/dev.vmware.yaml final_management.yml --skip-tags online_install,keepalived-install`

If you are rebuilding the RKE managed cluster then be sure to delete any existing RKE state file that may exist. These
can cause your cluster not to spin up with mysterious errors (especially if you've tried to keep the same elastic IPs!)

[NOTE] The cert_from_ca_intermediate_cert_pem param in ansible-rn/group_vars/type_env_dev/environments.yml determines the name of the CA root cert & key to use when creating the Rancher cert, e.g. rancher-intermediate.cert.pem

---
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
