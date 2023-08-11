#!/usr/bin/env python3
"upload.py -- maps action params to viam update + upload commands"

import argparse, os, subprocess, base64, logging, platform

# map platform.uname.machine -> GOARCH
ARCH_LOOKUP = {
    'x86_64': 'amd64',
    'aarch64': 'arm64',
}

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
    logging.basicConfig(level=logging.INFO)

    if args.cli_config_secret:
        os.makedirs(os.path.expanduser('~/.viam'))
        with open(os.path.expanduser('~/.viam/cached_cli_config.json'), 'wb') as fconfig:
            fconfig.write(base64.b64decode(args.cli_config_secret))
        logging.info('wrote cli secret')

    meta_args = ()
    if args.meta_path:
        meta_args = ('--module', args.meta_path)
    if args.org_id:
        org_args = ('--org-id', args.org_id)
    elif args.namespace:
        org_args = ('--public-namespace', args.namespace)
    else:
        raise Exception("shouldn't get here")

    command = f"viam-${ARCH_LOOKUP[platform.uname().machine]}"
    logging.info('selected command %s based on arch %s', command, platform.uname().machine)

    subprocess.check_call([command, 'version'])
    if args.do_update:
        subprocess.check_call([command, 'module', 'update', *meta_args, *org_args])
        logging.info('ran update')
    if args.do_upload:
        subprocess.check_call([command, 'module', 'upload', *meta_args, *org_args, '--platform', args.platform, '--version', args.version, args.module_path])
        logging.info('ran upload')

if __name__ == '__main__':
    main()
