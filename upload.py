#!/usr/bin/env python3
"upload.py -- maps action params to viam update + upload commands"

import argparse, os, subprocess, base64

def main():
    p = argparse.ArgumentParser(description='see action.yml for argument explanations')

    g1 = p.add_mutually_exclusive_group(required=True)
    g1.add_argument('--meta-path')
    g1.add_argument('--name')

    g2 = p.add_mutually_exclusive_group(required=True)
    g2.add_argument('--org-id')
    g2.add_argument('--namespace')

    p.add_argument('--module-path')
    p.add_argument('--cli-config-secret')
    p.add_argument('--platform')
    p.add_argument('--version')
    p.add_argument('--do-update', action='store_true')
    p.add_argument('--do-upload', action='store_true')
    args, _ = p.parse_known_args()

    if args.cli_config_secret:
        os.makedirs(os.path.expanduser('~/.viam'))
        with open(os.path.expanduser('~/.viam/cached_cli_config.json'), 'w') as fconfig:
            fconfig.write(base64.b64decode(args.cli_config_secret))

    meta_args = ()
    if args.meta_path:
        meta_args = ('--module', args.meta_path)
    if args.org_id:
        org_args = ('--org-id', args.org_id)
    elif args.namespace:
        org_args = ('--public-namespace', args.namespace)
    else:
        raise Exception("shouldn't get here")

    if args.do_update:
        subprocess.check_output(['viam', 'module', 'update', *meta_args, *org_args])
    if args.do_upload:
        subprocess.check_output(['viam', 'module', 'upload', *meta_args, *org_args, '--platform', args.platform, '--version', args.version, args.module_path])

if __name__ == '__main__':
    main()
