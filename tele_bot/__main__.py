'''This file will be executed like `python -m tele_bot -c config.json run`'''
import sys

def main():
    # We can use argparse module to receive config name and command (such as "run")
    # In config we need to store bot's api token and other stuff such as password to database
    print(sys.argv)

if __name__ == '__main__':
    main()

