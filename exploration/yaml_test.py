import os

import yaml

if __name__ == '__main__':

    # Test yaml loading
    with open(os.getcwd() + "/exploration/yaml_data/foo.yaml", 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        print(data)
