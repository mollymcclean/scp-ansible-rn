#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_ec2_node_template

short_description: This module handles managing rancher node templates

version_added: "1.1"

description:
    - "This module creates node templates in a given rancher install. Currently it will only deal with whether a named node template exists (creating it if it doesn't). In the future it should be expanded to check the properties of the returned node template and perform updates."

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
            - The name of the node template to create/update 
        required: true
    ami_id:
        description:
            - The name of the ami the node template should create instances with
        required: true
    vpc_id:
        description:
            - The name of the VPC the node template should create instances in 
        required: true
    subnet_id:
        description:
            - The name of the subnet the node template should create instances in (needs to be in the vpc above)
        required: true
    ssh_user:
        description:
            - The ssh user that should be used to log into the AMI
        required: true
    iam_instance_profile:
        description:
            - The IAM profile to authenticate against
        required: true
    ec2_size:
        description:
            - The size of the ec2 instances that should be created
        required: true
    ec2_tags:
        description:
            - The tags that should be associated with each ec2 instance
        required: true
    security_groups:
        description:
            - The security groups that should be associated with the instances
        required: true
    region:
        description:
            - The region to deploy the ec2 instances into 
        required: true
    region_zone:
        description:
            - The zone that the ec2 instances should be deployed into (must exist in the region above)
        required: true
    insecure_registries:
        description:
            - A list of any insecure registries that should be recognised by the machine.
        required: true
    access_key:
        description:
            - Choose the API key that will be used to launch the EC2 instance. 
        required: true
    block_duration_minutes:
        description:
            - AWS spot instance duration in minutes (60, 120, 180, 240, 300, or 360). Default 0 (string).
        required: false
    cloud_credential_id:
        description:
            - The ID or the Cloud Credentials that provide access to the cloud provider CLI.
        required: false
    device_name:
        description:
            - AWS root device name. Default /dev/sda1 (string)
        required: false
    encrypt_ebs_volumes:
        description:
            - Encrypt EBS Volume.
        required: true
    endpoint:
        description:
            - Optional endpoint URL (hostname only or fully qualified URI) (string).
        required: false
    engine_install_url:
        description:
            - The URL of the script that install docker. e.g. https://releases.rancher.com/install-docker/19.03.sh
        required: true
    insecure_transport:
        description:
            - Disables SSL when sending requests.
        required: true
    keypair_name:
        description:
            - The name assigned to the keypair being used to launch the EC2 instances.
        required: false
    monitoring:
        description:
            - Monitor, collect, and analyze instance metrics through Amazon CloudWatch. 
        required: true
    private_address_only:
        description:
            - Use only private IP address.
        required: true
    request_spot_instance:
        description:
            - Request an EC2 spot instance.
        required: true
    retries:
        description:
            - The number of retries of HTTP requests to AWS services.
        required: true
    root_size:
        description:
            - The size of the root disk to use.
        required: true
    security_group_readonly:
        description:
            - Whether or not the security group should be set to read only.
        required: true
    session_token:
        description:
            - The temporary session token to use for calls to the AWS SDK.
        required: false
    spot_price:
        description:
            - AWS spot instance bid price (in dollar). Default 0.50 (string).
        required: true
    use_ebs_optimized_instances:
        description:
            - Create an EBS optimized instance. Default false.
        required: true
    use_private_address:
        description:
            - Force the usage of private IP address. Default false.
        required: true
    userdata:
        description:
            - Specify the cloud-config YAML script as a single line. The correct YAML indentation must be maintained and \n used at the end of each line.
        required: false
    volume_type:
        description:
            - Specify the type of volume to use - gp2 (general purpose), io1 (provisioned IOPs) or Standard (Magnetic).
        required: true
    use_internal_ip_address:
         description:
            - Set to True so that the internal ports between EC2 instances are open to each other.
        required: true

author:
    - Guy
'''

EXAMPLES = '''
- name: Rancher EC2 Node Template Centos 7
  rancher_ec2_node_template:
    rancher_domain: rancher.cloudranger.co.uk
    api_bearer_token: token_export
    cloud_credential_id: XXXXXXXXXXXXXX
    name: My Node Template
    vpc_id: vpc-XXXXXXXXXXXXXXXXX
    subnet_id: subnet-XXXXXXXXXXXXXXXXX
    ami_id: ami-09e5afc68eed60ef4
    ssh_user: centos
    region: eu-west-2
    region_zone: a
    ami_id: ami-09e5afc68eed60ef4
    iam_instance_profile: RKECloudProvisioner
    security_groups:
      - rke_sg
    ec2_tags:
      Type: MyInstanceTag
    insecure_registries:
      - harbor.cloudranger.co.uk:80
    userdata: "#cloud-config\nruncmd:\n - [ sh, -xc, \"echo $(date) ': hello world!'" ]"
'''

RETURN = '''
node_template_id:
    description: The unique identifier for the node template
    type: string
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


class RancherEc2NodeTemplate(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            ami_id=dict(type='str', required=True),
            api_bearer_token=dict(type='str', required=True),
            block_duration_minutes=dict(type='int', default='0'),
            cloud_credential_id=dict(type='str', required=True),
            device_name=dict(type='str', default='/dev/sda1'),
            ec2_size=dict(type='str', default='t2.large'),
            ec2_tags=dict(type='dict', default={}),
            encrypt_ebs_volumes=dict(type='bool', default=False),
            endpoint=dict(type='str', required=False),
            engine_install_url=dict(type='str', required=True),
            iam_instance_profile=dict(type='str', required=True),
            insecure_registries=dict(type='list', elements='str', default=[]),
            insecure_transport=dict(type='bool', default=False),
            keypair_name=dict(type='str', required=False),
            monitoring=dict(type='bool', default=False),
            name=dict(type='str', required=True),
            private_address_only=dict(type='bool', default=False),
            rancher_domain=dict(type='str', required=True),
            region=dict(type='str', required=True),
            region_zone=dict(type='str', required=True),
            request_spot_instance=dict(type='bool', default=False),
            retries=dict(type='int',  default="5"),
            root_size=dict(type='int', default="80"),
            security_group_readonly=dict(type='bool', default=False),
            security_groups=dict(type='list', elements='str', required=True),
            session_token=dict(type='str', required=False),
            spot_price=dict(type='str', default="0.50"),
            ssh_user=dict(type='str', required=True),
            subnet_id=dict(type='str', required=True),
            use_ebs_optimized_instances=dict(type='bool', default=False),
            use_private_address=dict(type='bool', default=False),
            userdata=dict(type='str', required=False),
            use_internal_ip_address=dict(type='bool', default=True),
            validate_certs=dict(type='bool', default= False),
            volume_type=dict(type='str', default="gp2"),
            vpc_id=dict(type='str', required=True),
        )

        # Module input variables
        self.ami_id = None
        self.api_bearer_token = None
        self.block_duration_minutes = None
        self.cloud_credential_id = None
        self.device_name = None
        self.ec2_size = None
        self.ec2_tags = None
        self.encrypt_ebs_volumes = None
        self.endpoint = None
        self.engine_install_url = None
        self.iam_instance_profile = None
        self.insecure_registries = None
        self.insecure_transport = None
        self.keypair_name = None
        self.monitoring = None
        self.name = None
        self.private_address_only = None
        self.rancher_domain = None
        self.region = None
        self.region_zone = None
        self.request_spot_instance = None
        self.retries = None
        self.root_size = None
        self.security_group_readonly = None
        self.security_groups = None
        self.session_token = None
        self.spot_price = None
        self.ssh_user = None
        self.subnet_id = None
        self.use_ebs_optimized_instances = None
        self.use_private_address = None
        self.userdata = None
        self.use_internal_ip_address = None
        self.volume_type = None
        self.validate_certs = None
        self.vpc_id = None

        # Internal variables that aren't set through the module input
        self.path = '/v3/nodeTemplates/'

        self.results = dict(
            changed=False,
            node_template_id='',
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

        node_template_id = self.template_exists()

        if node_template_id is False:
            self.create_template()
        else:
            self.results['node_template_id'] = node_template_id

        return self.results

    def create_template(self):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'POST'

        tags_list = []

        if len(self.ec2_tags) != 0:
            for k,v in self.ec2_tags.items():
                tags_list.append(k + ',' + v)

        data = {
            'name': self.name,
            'amazonec2Config': {
                "ami": self.ami_id,
                "blockDurationMinutes": self.block_duration_minutes,
                "deviceName": self.device_name,
                "encryptEbsVolume": self.encrypt_ebs_volumes,
                "endpoint": self.endpoint,
                "iamInstanceProfile": self.iam_instance_profile,
                "insecureTransport": self.insecure_transport,
                "instanceType": self.ec2_size,
                "keypairName": self.keypair_name,
                "monitoring": self.monitoring,
                "privateAddressOnly": self.private_address_only,
                "region": self.region,
                "requestSpotInstance": self.request_spot_instance,
                "retries": self.retries,
                "rootSize": self.root_size,
                "securityGroup": self.security_groups,
                "securityGroupReadonly": self.security_group_readonly,
                "sessionToken": self.session_token,
                "spotPrice": self.spot_price,
                "sshUser": self.ssh_user,
                "subnetId": self.subnet_id,
                "tags": ','.join(tags_list),
                "useEbsOptimizedInstance": self.use_ebs_optimized_instances,
                "usePrivateAddress": self.use_private_address,
                "userdata": self.userdata,
                "validateCerts": self.validate_certs,
                "volumeType": self.volume_type,
                "vpcId": self.vpc_id,
                "zone": self.region_zone,
            },
            'engineInsecureRegistry': self.insecure_registries,
            "engineInstallURL": self.engine_install_url,
            "useInternalIpAddress": self.use_internal_ip_address,
            "cloudCredentialId": self.cloud_credential_id,
        }

        resp, info = fetch_url(self.module, self.rancher_domain + self.path, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 201:
            print(info);exit()
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' creating ec2 node template'

            self.module.fail_json(msg='Node Template Create request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())

        self.results['changed'] = True
        self.results['node_template_id'] = decoded_response['id']

    def template_exists(self):
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
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' listing existing templates'

            self.module.fail_json(msg='Node Template List request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())
        items = len(decoded_response['data'])

        # TODO: Check if there are other numbers of items returned and handle appropriately
        if items == 1:
            return decoded_response['data'][0]['id']

        return False


def main():
    RancherEc2NodeTemplate()


if __name__ == '__main__':
    main()
