## Create Certificate from Certificate Authority
This role generates a SSL certificate from a valid Certificate Authority and is expected to run on VMs in either the AWS
infrastructure where the CA has been pre-created and stored in an Amazon S3 bucket OR in HODC where the certs are stored
on the machine (and have been signed by the HSM in the environment)

## Example Usage
See the GitLab role usage in the `initial_management` play.
