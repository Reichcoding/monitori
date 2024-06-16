import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def get_config(section, key):
    return config[section][key]

def config_edit(section,key,value):
    config[section][key] = value
    with open('config.ini', 'w') as configfile:
        config.write(configfile)