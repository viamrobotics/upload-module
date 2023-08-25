# upload-module action

> [!NOTE]
> These are pre-release instructions for people who want to test this action, and will not work well yet for production flows.

This action uploads your module to the Viam modular registry. By default it runs both `update` (set your metadata) and `upload` (upload the module), but you can disable either step with configuration (see action.yml).

For more information about the parameters, look at:
- [action.yml](./action.yml)
- `viam module update --help` and `viam module upload --help` in our CLI

Or keep reading for a tutorial.

## Basic usage

1. Go to the 'Actions' tab of your repo -> 'create a new workflow' -> 'set up yourself'
1. Paste in the following YAML, then edit all the lines marked with `<--`
1. Follow the 'setting CLI config secret' instructions [below](#setting-cli-config-secret)
1. Push to a branch or create a release -- your module should upload to our registry with the appropriate version

```yml
on:
  push:
  release:
    types: [released]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: build
      run: echo "your build command goes here" && false # <-- replace this with the command that builds your module's tar.gz
    - uses: viamrobotics/upload-module@main
      # if: github.event_name == 'release' # <-- once the action is working, uncomment this so you only upload on release
      with:
        module-path: module.tar.gz
        org-id: your-org-id-uuid # <-- replace with your org ID. not required for public modules
        platform: linux/amd64 # <-- replace with your target architecture, or your module will not deploy
        version: ${{ github.event_name == 'release' && github.ref_name || format('0.0.0-{0}.{1}', github.ref_name, github.run_number) }} # <-- see 'Versioning' section below for explanation
        cli-config-secret: ${{ secrets.cli_config }}
```

## Setting CLI config secret

> [!NOTE]
> These are pre-release instructions for testing this action, and will not work well for production flows. These instructions will give you a short lived access token that cannot self-update after its first refresh. Stay tuned.

Base64-encode your CLI secret by running:

```sh
# run this on the device where you installed the `viam` CLI
cat ~/.viam/cached_cli_config.json | base64
```

(If that json file doesn't exist, run `viam login` first).

Then:
- copy the output of that command to the clipboard
- go to 'Settings' -> 'Secrets and variables' -> 'Actions' in your repo
- click the 'New repository secret' button
- name your secret `cli_config` (so it agrees with `secrets.cli_config` in the sample YAML)
- paste the base64 output into the secret body

The publish job will run on your next release. You can trigger a re-run of a previous failed job from your repo's 'Actions' tab.

## Versioning

The version string in the yaml above is:

```js
github.event_name == 'release'
  && github.ref_name
  || format('0.0.0-{0}.{1}', github.ref_name, github.run_number)
```

That will do the following:

| event | action
|---|---
| release | version the module with your release tag (a semver string you set manually)
| push | version the module like `0.0.0-main.10` ('main' is the branch name)

This uploads the latest run from any branch if needed for testing.

## Example repos

- [publish.yml in zipapp-module](https://github.com/viamrobotics/zipapp-module/blob/main/.github/workflows/publish.yml) (python)
