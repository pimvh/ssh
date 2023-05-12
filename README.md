# Requirements

1. Ansible installed:

```
sudo apt install python3
python3 -m ensurepip --upgrade
pip3 install ansible
```

## Required variables

Review the variables as shown in defaults.

A description of what the variables entails is included in the argument specification (see meta/main.yaml).

```
---
ssh_directory: /etc/ssh
ssh_config_file: "{{ ssh_directory }}/sshd_config"
ssh_trusted_user_ca_keys_file: "{{ ssh_directory }}/ssh_trusted_user_ca_keys"

ssh_acceptable_hostkey_crypto:
  - rsa
  - ecdsa
  - ed25519

ssh_copy_trusted_user_cas: true
ssh_sign_host_certificate: true
ssh_add_host_certificate_to_known_hosts: true

# ssh config options
ssh_print_motd: true
ssh_permit_root_login: false

ssh_host_certificate_validity: "" # 2w for 2 weeks
# lookups work well for keys, like "{{ lookup('ansible.builtin.file', '....pub') }} }}" or lookup('ansible.builtin.vars', '....') }}
# but it depends on your usage
# take care that your resulting key is formatted correctly (e.g. it has a trailing newline)
ssh_host_ca_public_key: ""
ssh_host_ca_private_key: ""
ssh_host_ca_private_key_pass: ""

ssh_trusted_user_ca_keys: []
# - "key1"
# - "key2"

ssh_authorized_principals: []
# - user: johndoe
#   principals:
#     - john
#     - doe
# - user: root
#   principals:
#     - all
#     - root

ssh_host_domain: ""

ssh_revoked_keys: []

ssh_match_directives: []
# For example:
# - note: Permit Root from certain IP
#     rule: Address 10.10.10.10
#     results:
#   - PermitRootLogin prohibit-password

```

The ansible playbook will validate whether the correct variables are passed to the role using an argument_spec.

# Example playbook

Minimal (assuming you passed variables elsewhere):

```
hosts:
  - foo
roles:
  - pimvh.ssh

```

# TLDR - What will happen if I run this

- validate certain nested variables
- configure the user SSH Certificate Authority
  - gather the host keys from the system
  - sign the current hostkeys with the passed ssh_host_key
  - add the certificate to the controllers known_hosts file
  - gather the found certificates
- configure the host SSH Certificate Authority
  - move the trusted user Certificate public key to the host
  - make the authorized principle directory, and create mapping from principals to users
  - add revoked keys
- template the sshd configuration file

# Future Improvements

- consider move logic to scripts instead of using Ansible tasks
- allow hostkey rollover directives
