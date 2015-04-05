# write-dpxdt-configuration
small python-helper to generate a set of dxpdt-test-configuration-files for a common set of urls


## Installation

* clone this repository
* cd into it and run `pip install -r requirements.txt`

## Usage

* Run the command via `pyhton write-dpxdt-configuration.py <path-to-your-master-configguration-file>`

## The master-configuration-file

The master configuration file stores a set of configurations and a set of urls. The python-utility will create a dpxdt-test-configuration for every configuration found in the master-file, adding all urls as tests for the specific configuration. You can overwrite the config for a given url via a separate config-settings for this url

## Example:

```
output_folder: dpxdt-tests

base_url: http://target

setup: |
  echo "nothing to do"

waitFor:
  url: /
  timeout_secs: 5

base_config: &base_config
  injectCss: >
    body {
      background-color: white;
    }

configs:
  palm:
    <<: *base_config
    viewportSize:
      width: 320
      height: 480

  lap-portrait:
    <<: *base_config
    viewportSize:
      width: 768
      height: 1024

  lap-landscape:
    <<: *base_config
    viewportSize:
      width: 1024
      height: 768
  desk:
    <<: *base_config
    viewportSize:
      width: 1280
      height: 800

tests:
  - url: /de
  - url: /en
  - url: /de/newsletter
    name: newsletter-test
    config:
      injectCss: >
        body { background-color: #f00; }
      injectJs: |
        alert("does work");

```

This example wil create four yaml-file in the folder `dpxdt-tests`, with four different viewport-sizes. It prefixes every url with the `base_url`-setting.

