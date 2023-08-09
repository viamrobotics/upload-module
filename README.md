# upload-module action

This action uploads your module to the Viam modular registry. By default it runs both `update` (set your metadata) and `upload` (upload the module), but you can disable either step with configuration (see action.yml).

For more information about the parameters, look at:
- [action.yml](./action.yml)
- `viam module update --help` and `viam module upload --help` in our CLI

## Basic usage

```yml
on:
  push:

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: build
      run: make module.tar.gz # <-- your build command goes here
    - name: upload
      uses: viamrobotics/upload-module@main
      with:
        module-path: module.tar.gz
        org-id: ${{ secrets.org-id }}
        platform: linux/amd64
        version: ${{ github.ref_name }}
        cli-config-secret: ${{ secrets.cli_config }}

```

## Setting CLI config secret

Base64-encode your CLI secret by running:

```sh
cat ~/.viam/cached_cli_config.json | base64
```

If that json file doesn't exist, run `viam login` first.

Then set a secret by visiting the secrets page for your repo: https://github.com/.../.../settings/secrets/actions. (Replace the ...).

## Example repos

- [publish.yml in zipapp-module](https://github.com/viamrobotics/zipapp-module/blob/main/.github/workflows/publish.yml) (python)
