from src.settings import AppSettings
import os

def main():
    command = 'sanic src.server:app --fast'
    if AppSettings.DEBUG:

        command += ' --debug --reload'
    os.system(command=command)


if __name__ == '__main__':
    main()
