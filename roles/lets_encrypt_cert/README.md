## Let's Encrypt Certificate
This role generates a let's encrypt certificate and is expected to run on VMs in the AWS infrastructure where we need
free certificates that have trust associated in the browser.

By default the role runs against the Staging Environment of let's encrypt. Once you have tested integrating the role
with your application you should change it to run as production

Currently, this role delegates the route 53 creation to be run on the machine that runs ansible. This means user laptops
at the moment. This means that this role has a dependency of the python `boto` library being installed
(as documented in the README.md of the main repo). In the future we can with the right role delegations run this on the
VMs themselves in AWS so they request their own certificate renewals (triggered by some sort of Lambda)

## Example Usage
See the GitLab role usage in the `initial_management` play.
