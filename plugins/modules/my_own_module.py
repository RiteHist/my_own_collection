#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This is my module for creating a file.

version_added: "1.0.0"

description: This module creates a .txt file with the specified content on the target hosts.

options:
    filename:
        description: This is the name of the file without an extension.
        required: true
        type: str
    path:
        description: The directory path where the file will be created.
        required: true
        type: str
    content:
        description: The contents to write into the file.
        required: true
        type: str
    overwrite:
        description: An option to overwrite the file if it's already exists.
        required: false
        type: bool
author:
    - Gregory Wright (@RiteHist)
'''

EXAMPLES = r'''
- name: Use my_own_module
    my_own_module:
        filename: "cool_file"
        path: "/tmp"
        content: "Very nice"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'File already exists with the same content. No changes made.'
'''

from ansible.module_utils.basic import AnsibleModule
import os


def create_file(result: dict) -> dict:
    filename = result['filename'] + '.txt'
    filepath = os.path.join(result['path'], filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            if f.read() == result['content'] and not result['overwrite']:
                result['message'] = 'File already exists with the same content. No changes made.'
                return result
    
    result['changed'] = True
    if not os.path.exists(result['path']):
        os.makedirs(result['path'])
    with open(filepath, 'w') as f:
        f.write(result['content'])
    
    result['message'] = 'File created/overwritten successfully.'
    return result

def run_module():
    module_args = dict(
        filename=dict(type='str', required=True),
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        overwrite=dict(type='bool', required=False, default=False)
    )

    result = dict(
        changed=False,
        filename='',
        path='',
        content='',
        message='',
        overwrite=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    result['filename'] = module.params['filename']
    result['path'] = module.params['path']
    result['content'] = module.params['content']
    result['overwrite'] = module.params['overwrite']
    
    if module.check_mode:
        module.exit_json(**result)

    try:
        result = create_file(result)
    except Exception as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()