import os

import yaml

if __name__ == '__main__':

    # Test yaml loading
    with open(os.getcwd() + "/exploration/yaml_data/foo.yaml", 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        print(data)

    # Test yaml dumping
    users = [{'name': 'John Doe', 'occupation': 'gardener'},
             {'name': 'Lucy Black', 'occupation': 'teacher'}]
    with open(os.getcwd() + "/exploration/yaml_data/write.yaml", 'w') as f:
        data = yaml.dump(users, f)
