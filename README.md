# upload-module action

This action uploads your module to the Viam modular registry. By default it runs 

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

## Example repos

- [publish.yml in zipapp-module](https://github.com/viamrobotics/zipapp-module/blob/main/.github/workflows/publish.yml) (python)
