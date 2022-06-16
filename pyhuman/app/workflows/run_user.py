import subprocess
import sys
from time import sleep
import os
import random

from ..utility.base_workflow import BaseWorkflow


WORKFLOW_NAME = 'Run User activity'
WORKFLOW_DESCRIPTION = 'Run user activity to interact with host operating system'


def load():
    return RunUser()

class RunUser(BaseWorkflow):
    def __init__(self):
        super().__init__(name=WORKFLOW_NAME, description=WORKFLOW_DESCRIPTION)
        self.userbehavior={1:'Create a file within a directory',2:'Create a directory within a directory.',
                           3:'Move a file within a directory.',4:'Move a directory within a directory.',5:'Delete a file from a directory.',
                           6:'Delete a directory from a directory.',7:'Modify a file within a directory.',8:'Modify a directory. '}

    def action(self, extra=None):
        self._run_user_and_quit()

    """ PRIVATE """

    def _run_user_and_quit(self):
        p = subprocess.Popen("cmd.exe /C " + self._determine_behavior(), shell=True)
        sleep(5)
        p.kill()

    def _determine_behavior(self):
        chosen_behavior=self._get_random_behavior()
        if chosen_behavior==1:
            f,_,w=self._load_behavior()
            return 'type ' + w + ' > ' + 'C:\\Users\\IEUser\\Documents\\'+ f
        elif chosen_behavior==2:
            _, d, _ = self._load_behavior()
            return 'mkdir C:\\Users\\IEUser\\Documents\\' + d
        elif chosen_behavior==3:
            original_file, _, _ = self._load_behavior()
            new_file, _, _ = self._load_behavior()
            return 'move C:\\Users\\IEUser\\Documents\\' + original_file + 'C:\\Users\\IEUser\\Documents\\' +new_file
        elif chosen_behavior == 4:
            original_dir, _, _ = self._load_behavior()
            new_dir, _, _ = self._load_behavior()
            return 'move C:\\Users\\IEUser\\Documents\\' + original_dir + 'C:\\Users\\IEUser\\Desktop' + new_dir
        elif chosen_behavior == 5:
            f, _, _ = self._load_behavior()
            return 'del C:\\Users\\IEUser\\Documents\\' + f
        elif chosen_behavior == 6:
            _, d, _ = self._load_behavior()
            return 'rmdir /S C:\\Users\\IEUser\\Documents\\' + d
        elif chosen_behavior == 7:
            f,_,w=self._load_behavior()
            return 'echo ' + w + ' > ' + 'C:\\Users\\IEUser\\Documents\\'+ f
        elif chosen_behavior == 8:
            original_dir, _, _ = self._load_behavior()
            new_dir, _, _ = self._load_behavior()
            return 'move C:\\Users\\IEUser\\Desktop\\' + original_dir + 'C:\\Users\\IEUser\\Documents\\' + new_dir
        else:
            print(f'Incorrect chosen behavior: {chosen_behavior}')

    def _get_random_behavior(self):
        return random.choice(list(self.userbehavior.keys()))

    @staticmethod
    def _load_behavior():
        random_file=random.choice(open('../../data/file_options.txt').read().splitlines())
        random_dir = random.choice(open('../../data/dir_options.txt').read().splitlines())
        random_words=random.choice(open('../../data/echo_words.txt').read().splitlines())
        return random_file,random_dir,random_words





