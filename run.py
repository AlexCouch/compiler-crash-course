import os
import subprocess

cwd = os.getcwd()

samples_path = os.path.abspath(os.getcwd() + '/samples')
os.chdir(os.path.abspath(os.getcwd() + '/src'))

command = subprocess.run(['python', 'main.py', samples_path + '/test.em'])
