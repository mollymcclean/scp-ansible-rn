#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2016 John Buxton <john.buxton2@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: chage
short_description: query & manage shadow password file on Linux
description:
    - manage shadow password file on Linux
    - one user at a time
    - calls chage command to make changes
    - returns user shadow settings as a dict
    - for detailed information on shadow file & chage command see:
        - /usr/include/shadow.h
        - man chage
        - pydoc spwd
    - dates must be in the form YYYY-MM-DD

notes: []
version_added: null
author:
    - 'John Buxton (@lqueryvg)'
options:
    user:
        required: true
        description:
          - user name

    sp_lstchg:
        required: false
        default: null
        description:
          - days since 1970/01/01 when password was last changed
            or date in format YYYY-MM-DD
          - chage option = -d, --lastday
        aliases: [ lastday ]

    sp_min:
        required: false
        default: null
        description:
          - set minimum number of days between changes
          - chage option = -m, --mindays
        aliases: [ mindays ]

    sp_max:
        required: false
        default: null
        description:
          - set maximum number of days between changes
          - chage option = -M, --maxdays
          - remove the field by passing value of -1
        aliases: [ maxdays ]

    sp_warn:
        required: false
        default: null
        description:
          - set number of days before password expiry
            to warn user to change the password
          - chage option = -W, --warndays
        aliases: [ warndays ]

    sp_inact:
        required: false
        default: null
        description:
          - set number of days the account may be inactive
          - chage option = -I, --inactive
          - remove the field by passing value of -1
        aliases: [ inactive ]

    sp_expire:
        required: false
        default: null
        description:
          - set number of days since 1970-01-01 until account expires
            or date in format YYYY-MM-DD
          - chage option = -E, --expiredate
          - remove the field by passing value of -1
        aliases: [ expiredate ]
"""

EXAMPLES = """
# force password change on next login
- chage: user=john sp_lstchg=0
# or:
- chage: user=john lastday=0

# remove an account expiration date.
- chage: user=john sp_expire=-1
# or using argument alias:
- chage: user=john expiredate=-1

# set inactivity days after password expired before account is locked
- chage: user=john sp_inact=14

# set both min and max days in single task
- chage: user=john sp_min=7 sp_max=28

# display user password warn days
- chage: user=john
  register: shadow_data
- debug: msg={{shadow_data.sp_warn}}
"""


def _convert_date(str):  # convert YYYY-MM-DD to days since 1/1/1970
    from datetime import date
    (y, m, d) = str.split('-')
    delta = date(int(y), int(m), int(d)) - date(1970, 1, 1)
    return delta.days


def main():
    module = AnsibleModule(
        argument_spec=dict(
            user=dict(required=True),
            sp_lstchg=dict(required=False, aliases=['lastday'], default=None),
            sp_min=dict(required=False, aliases=['mindays'], default=None),
            sp_max=dict(required=False, aliases=['maxdays'], default=None),
            sp_warn=dict(required=False, aliases=['warndays'], default=None),
            sp_inact=dict(required=False, aliases=['inactive'], default=None),
            sp_expire=dict(required=False, aliases=['expiredate'], default=None),
        ),
        supports_check_mode=True
    )

    user = module.params['user']

    current_shadow = None
    try:
        f = open('/etc/shadow', 'r')
    except IOError as err:
        message = "unable to open /etc/shadow, I/O error(%s): %s" % (err.errno, err.strerror)
        module.fail_json(msg=message)

    for line in f.readlines():
        line = line.rstrip()
        fields = line.split(':')
        if fields[0] == user:
            current_shadow = dict(zip(
                ['sp_nam', 'sp_pwd', 'sp_lstchg', 'sp_min', 'sp_max',
                 'sp_warn', 'sp_inact', 'sp_expire', 'sp_flag'],
                fields
            ))
            break

    f.close()

    if current_shadow is None:
        message = "unable to find user %s in /etc/shadow" % user
        module.fail_json(msg=message)

    chage_flags = dict(
        sp_lstchg='--lastday',
        sp_min='--mindays',
        sp_max='--maxdays',
        sp_warn='--warndays',
        sp_inact='--inactive',
        sp_expire='--expiredate',
    )

    # Start building 'chage' command to make changes.
    cmd = []

    # build return value in case command is successful
    new_shadow = current_shadow

    import re
    date_pattern = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")

    for param_name, flag_name in chage_flags.items():
        desired_value = module.params[param_name]
        desired_cmd_value = desired_value

        # Only add flags for parameters that need to be changed.
        # check if desired_value different from current value
        if desired_value is not None:

            if param_name in ['sp_expire', 'sp_inact', 'sp_max'] \
                    and desired_value == "-1":
                desired_value = ""

            if param_name in ['sp_lstchg', 'sp_expire'] \
                    and desired_value != "" \
                    and date_pattern.match(desired_value):
                desired_value = str(_convert_date(desired_value))

            if desired_value != current_shadow[param_name]:
                # need to make a change, so append correct options
                cmd.append(flag_name)
                cmd.append(desired_cmd_value)
                new_shadow[param_name] = desired_value

    # were any changes needed ?
    if cmd.__len__() == 0:
        # no changes needed
        module.exit_json(shadow=current_shadow, changed=False)

    if module.check_mode:
        module.exit_json(shadow=new_shadow, changed=True)

    # complete command and run it
    cmd.insert(0, module.get_bin_path('chage', required=True))
    cmd.append(user)
    (rc, out, err) = module.run_command(cmd)

    # fail if command didn't work
    if rc is not None and rc != 0:
        module.fail_json(msg=err, rc=rc)

    # command succeeded, so return the updated shadow entry
    module.exit_json(shadow=new_shadow, changed=True)


from ansible.module_utils.basic import *

main()