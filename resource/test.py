import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    file = config.read("user.ini")
    config_dict = config.defaults()
    print(config_dict['user_name'])
    print("ooo")