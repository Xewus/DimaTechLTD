from src.settings import DEBUG
import os

def main():
    command = 'sanic src.api.server:app'
    if DEBUG:
        command += ' --debug --reload'
    os.system(command=command)


if __name__ == '__main__':
    main()
