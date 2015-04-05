import os.path
import argparse
import yaml
import copy

from pprint import pprint

def data_merge(a, b):
  output = {}
  for item, value in a.iteritems():
    if b.has_key(item):
      if isinstance(b[item], dict):
        output[item] = data_merge(value, b.pop(item))
    else:
      output[item] = copy.deepcopy(value)
  for item, value in b.iteritems():
    output[item] = copy.deepcopy(value)
  return output

def main():

  parser = argparse.ArgumentParser(description='Write dpxdt-test configuration-files.')
  parser.add_argument('file',help='file with dpxdt-presets',action='store')

  args = parser.parse_args()

  yaml_file = open(args.file, "r")
  configuration =  yaml.load(yaml_file)

  for config_name in configuration['configs']:
    config = configuration['configs'][config_name]

    test_config = {}
    test_config['setup'] = configuration['setup']
    test_config['waitFor'] = copy.deepcopy(configuration['waitFor'])
    test_config['waitFor']['url'] = configuration['base_url'] + configuration['waitFor']['url']
    test_config['tests'] = []

    for test in configuration['tests']:
      result = {}

      if not 'name' in test:
        result['name'] = test['url'].replace('/','-')
      else:
        result['name'] = test['name']

      result['name'] = config_name.replace('_','-') + '-' + result['name']
      result['url'] = configuration['base_url'] + test['url']

      if 'config' in test:
        result['config'] = data_merge(config, test['config'])
      else:
        result['config'] = config

      test_config['tests'].append(result)

    # write yaml-file
    outfilename = configuration['output_folder'] + "/" + config_name + ".yaml"
    print "Writing configuration into " + outfilename

    outfile = open(outfilename, "w")
    outfile.write( yaml.dump(test_config, default_flow_style=False) )



if __name__ == "__main__":
    main()
