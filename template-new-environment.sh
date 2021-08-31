#!/bin/bash

set -eux

usage(){
    cat << EOF >&2
Usage: ${0} <environment name>
e.g.: ${0} preprod
Usage: ${0} <rnvironment name (No dashes in the name. Underscores are OK)>
e.g. ${0} dev
e.g. ${0} devops_tooling

Configures Ansible variables for a deployment based on shell
environment varaibles.
EOF
}

die(){
    echo "$1" >&2
}

echo "${INTERNAL_IP_RANGE}"
echo "${APT_MIRROR}"
echo "${DNS_SERVER_ADDR}"
echo "${NTP_SERVER_ADDR}"
echo "${CORE_ROUTER_ADDR}"

echo "${VCENTER_DOMAIN}"
echo "${VCENTER_DEPLOY_USERNAME}"
echo "${VCENTER_DEPLOY_PASSWORD}"

echo "${VCENTER_RKE_USERNAME}"
echo "${VCENTER_RKE_PASSWORD}"

echo "${VSPHERE_DC}"
echo "${VSPHERE_CLUSTER}"
echo "${VSPHERE_VM_FOLDER}"
echo "${VSPHERE_DATASTORE_NAME}"
echo "${VSPHERE_INTERNAL_NETWORK}"
echo "${VSPHERE_RESOURCE_POOL}"

echo "${VSPHERE_ENV_TAG_URN}"
echo "${VSPHERE_CLUSTER_TAG_URN}"
echo "${VSPHERE_WORKER_NODE_TAG_URN}"

export NETWORK_FIRST_THREE_OCTETS="${INTERNAL_IP_RANGE%\.[0-9]*\/24}"
export VM_ENV="$(echo ${1} | sed 's/_/-/g')"
export POSTGRES_KEEPALIVED_PASSWORD=$(pwgen 21 1)
export REDIS_KEEPALIVED_PASSWORD=$(pwgen 21 1)
export HARBOR_KEEPALIVED_PASSWORD=$(pwgen 21 1)
export HARBOR_LDAP_SEARCH_PASSWORD=$(pwgen 21 1)
export HARBOR_POSTGRES_PASSWORD=$(pwgen 21 1)
export POSTGRES_REPL_PASSWORD=$(pwgen 21 1)
export POSTGRES_SUPERUSER_PASSWORD=$(pwgen 21 1)
export REDIS_PASSWORD=$(pwgen 21 1)
export REDIS_SENTINEL_PASSWORD=$(pwgen 21 1)
export SSH_AD_JOIN_PASSWORD=$(pwgen 21 1)
export HARBOR_RANCHER_PASSWORD=$(pwgen 21 1)

export RKE_ADMIN_PASSWORD=$(pwgen 21 1)
export HARBOR_ADMIN_PASSWORD=$(pwgen 21 1)

echo "Harbor credentials: admin / ${HATBOR_ADMIN_PASSWORD}"
echo "Rancher credentials: admin / ${RKE_ADMIN_PASSWORD}"

for TEMPLATE in $(find $(dirname ${0})/group_vars/type_env_${1} -name '*\.template'); do
  YAML_NAME="$TEMPLATE%\.template}"
  [[ -f "$YAML_NAME" ]] && die "Safety check: ${YAML_NAME} already exists. Will not overwrite. Please backup and delete before restarting."
  cat ${TEMPLATE} | envsubst > ${YAML_NAME}
  echo "Templated ${YAML_NAME}: Please save this for future use."
done

for TEMPLATE in $(find $(dirname ${0})/inventory/${1} -name '*\.template'); do
  YAML_NAME="$TEMPLATE%\.template}"
  [[ -f "$YAML_NAME" ]] && die "Safety check: ${YAML_NAME} already exists. Will not overwrite. Please backup and delete before restarting."
  cat ${TEMPLATE} | envsubst > ${YAML_NAME}
  echo "Templated inventory file ${YAML_NAME}"
done

echo "----"
echo "Completed"