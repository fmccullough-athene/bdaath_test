import sys

'''
This is how you add your own methods.
Create a folder, and place your classes inside the folder. Then add the folder to your sys.path, and import.
'''
sys.path.insert(0, "./ExampleProject")
from ExampleProject.exampleclass import example_class


import configparser as cfg
import argparse


def load_config():
    Config = cfg.ConfigParser()
    '''
    Place local.conf in the 'conf' folder of your project
    '''
    Config.read(r'.\conf\local.conf')
    '''
    Place resources.conf in the path defined by the 'resource_conf_file' setting in the local.conf file.
    This should be: C:/Development/Python/conf/resources
    '''
    resourcepath = Config.read(Config['Settings']['resource_conf_file'])

    print("load_config: ", resourcepath)

    return Config

def example_of_using_class(string):
    '''
    These are some examples of how to use a method from an imported class.
    '''
    example_class.example_method()
    example_class.second_example_method(string)
    print(example_class.second_example_method(string))
    return

''''
This defines the 'main' method.
'''
def main():

    print("Here1")

    parser = argparse.ArgumentParser()
    '''
    This is where your arguments are defined.
    '''
    parser.add_argument("-a", "--argument", help="this is an argument")
    
    args = parser.parse_args()

    '''
    Set a variable to the value of your argument, for use later in the program.
    '''
    argument_value = args.argument
    
    '''
    Load values from your config.
    '''
    print("Here1")

    Config = load_config()

    
    
    '''
    This is how to get the connection string:
    Get the path to the db_SQL_AHLDW_prod file, which contains the connection string.
    '''
    print("Here2")

    Config.read(Config['Resources']['db_SQL_AHLDW_prod'])

    #print("From Resources db_SQL_AHLDW_prod: ", viewit1)

    '''
    Now you can access the connection_string
    '''
    connection_string = Config['Resource']['connection_string']
    print (connection_string)


    print(f'This is an example of accessing an argument: {argument_value}')
    example_of_using_class(argument_value)




'''
This is where the program begins running.
'''
if __name__ == '__main__':
    '''
    When the program starts, it runs the 'main' method.
    '''
    print("Starting")

    main()

