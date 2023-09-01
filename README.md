# upload-module action

This action uploads your module to the Viam modular registry. By default it runs both `update` (set your metadata) and `upload` (upload the module), but you can disable either step with configuration (see action.yml).

For more information about the parameters, look at:
- [action.yml](./action.yml)
- `viam module update --help` and `viam module upload --help` in our CLI

Or keep reading for a tutorial.

## Basic usage

1. Go to the 'Actions' tab of your repo -> 'create a new workflow' -> 'set up yourself'
1. Paste in the following YAML, then edit all the lines marked with `<--`
1. Follow the 'setting up auth' instructions [below](#setting-up-auth)
1. Push a commit or create a release -- your module should upload to our registry with the appropriate version

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
        key-id: ${{ secrets.viam_key_id }}
        key-value: ${{ secrets.viam_key_value }}
```

## Setting up auth

1. Run `viam organizations list` to view your organization ID.
2. Create a key with `viam organization api-key create --org-id $YOUR_ORG_UUID --name pick-any-name`. This command outputs an ID + a value, both of which you will use in step 4 below.
3. In the github repo for your project, go to 'Settings' -> 'Secrets and variables' -> 'Actions'
4. Create two new secrets using the 'New repository secret' button:
  - `viam_key_id` with the UUID from "Key ID:" in your terminal
  - `viam_key_value` with the string from "Key Value:" in your terminal
5. All set! If you copy the YAML example above, it will use these secrets to authenticate to Viam. If you have already tried the action and it failed because the secrets were missing, you can trigger a re-run from your repo's 'Actions' tab.
from your repo's 'Actions' tab.

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
