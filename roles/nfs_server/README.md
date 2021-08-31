Ansible Role: NFS Server
=========

Ansible role to install and configure NFS server.

Through a simple list, you can indicate the directories to share, their NFS options, and the networks that have access to them.

Easy use of IPv6 addresses, brackets are added automatically when necessary using the `ipwrap` filter.

Requirements
------------

#### Ansible version:
Ansible \>= 2.7

#### Python libraries:
- `netaddr` to use IP address filter.
- `jmespath` to use JSON query filter.


Role Variables
--------------

```yaml
exports:    # Full list of directories to export
  - path: /var/helloWorld  # Complete path to the first directory to share
    parameters: rw,secure,sync,no_subtree_check,no_root_squash  # NFS sharing options
    networks:
      - 192.168.0.0/255.255.255.0 	# Network allowed to access to this directory
```

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
    - role: nfs_server
      exports:
        - path: /var/shared
          parameters: rw,secure,sync,no_subtree_check,no_root_squash
          networks: 
            - 192.168.0.0/255.255.255.0
```