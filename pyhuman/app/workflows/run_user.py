import subprocess
import sys
from time import sleep
import os
import random

from ..utility.base_workflow import BaseWorkflow


WORKFLOW_NAME = 'Run User activity'
WORKFLOW_DESCRIPTION = 'Run user activity to interact with host operating system via command line (cmd.exe)'


def load():
    return RunUser()

class RunUser(BaseWorkflow):
    def __init__(self):
        super().__init__(name=WORKFLOW_NAME, description=WORKFLOW_DESCRIPTION)
        self.userbehavior={1:'Create a file within a directory',2:'Create a directory within a directory.',
                           3:'Move a file within a directory.',4:'Move a directory within a directory.',5:'Delete a file from a directory.',
                           6:'Delete a directory from a directory.',7:'Modify a file within a directory.'}

    def action(self, extra=None):
        self._run_user_and_quit()

    """ PRIVATE """

    def _run_user_and_quit(self):
        p = subprocess.Popen("cmd.exe /C " + self._determine_behavior(), shell=True)
        sleep(5)
        p.kill()

    def _determine_behavior(self):
        chosen_behavior=self._get_random_behavior()
        if chosen_behavior==1: #Create a file within documents directory
            f,_,w=self._load_behavior()
            return 'echo ' + w + ' > ' + 'C:\\Users\\IEUser\\Documents\\'+ f
        elif chosen_behavior==2: #Create a directory within documents directory.
            _, d, _ = self._load_behavior()
            return 'mkdir C:\\Users\\IEUser\\Documents\\' + d
        elif chosen_behavior==3: #Move a file within documents directory.
            original_file, _, w = self._load_behavior()
            new_file, _, _ = self._load_behavior()
            if not (self._check_file_exist(original_file)):
                make_p = subprocess.Popen("cmd.exe /C echo " + w + " >  C:\\Users\\IEUser\\Documents\\" + original_file, shell=True)
                sleep(2)
                make_p.kill()
            return 'move C:\\Users\\IEUser\\Documents\\' + original_file + 'C:\\Users\\IEUser\\Documents\\' +new_file
        elif chosen_behavior == 4: #Move a directory within another documents directory.
            _, firstdir, _ = self._load_behavior()
            _, seconddir, _ = self._load_behavior()
            if not (self._check_dir_exist(firstdir)):
                make_p = subprocess.Popen("cmd.exe /C mkdir C:\\Users\\IEUser\\Documents\\" + firstdir, shell=True)
                sleep(2)
                make_p.kill()
            return 'mkdir C:\\Users\\IEUser\\Documents\\' + firstdir + "\\"+ seconddir
        elif chosen_behavior == 5: #Delete a file from documents directory.
            f=self._retrieve_file()
            return 'del C:\\Users\\IEUser\\Documents\\' + f
        elif chosen_behavior == 6: #Delete a directory from a directory.
            d=self._retrieve_file()
            return 'rmdir /S C:\\Users\\IEUser\\Documents\\' + d
        elif chosen_behavior == 7: #Modify a file within documents directory
            f,_,w=self._load_behavior()
            if not (self._check_file_exist(f)):
                make_p = subprocess.Popen("cmd.exe /C echo " + w + " >  C:\\Users\\IEUser\\Documents\\" + f, shell=True)
                sleep(2)
                make_p.kill()
            return 'echo ' + w + ' > ' + 'C:\\Users\\IEUser\\Documents\\'+ f
        else: #if there isnt a correct behavior chosen
            print(f'Incorrect chosen behavior: {chosen_behavior}')

    def _get_random_behavior(self):
        return random.choice(list(self.userbehavior.keys()))

    def _check_file_exist(self,input_file):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'created_files.txt')), 'w') as f:
            if input_file in f.read():
                return True
            else:
                f.write(input_file)
                return False

    def _check_dir_exist(self,input_dir):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'created_dirs.txt')), 'w') as d:
            if input_dir in d.read():
                return True
            else:
                d.write(input_dir)
                return False

    @staticmethod
    def _load_behavior():
        random_file=random.choice(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', 'file_options.txt')), 'r').read().splitlines())
        random_dir = random.choice(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', 'dir_options.txt')), 'r').read().splitlines())
        random_words=random.choice(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', 'echo_words.txt')), 'r').read().splitlines())
        return random_file,random_dir,random_words

    @staticmethod
    def _retrieve_file():
        return random.choice(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', 'created_files.txt')), 'r').read().splitlines())
    @staticmethod
    def _retrieve_dir():
        return random.choice(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', 'created_dirs.txt')), 'r').read().splitlines())



