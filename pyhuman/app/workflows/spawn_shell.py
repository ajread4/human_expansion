import subprocess
import sys
from time import sleep
import os
import random

from ..utility.base_workflow import BaseWorkflow


WORKFLOW_NAME = 'Spawn Shell'
WORKFLOW_DESCRIPTION = 'Spawn shell and run commands'


def load():
    return SpawnShell()


class SpawnShell(BaseWorkflow):

    def __init__(self):
        super().__init__(name=WORKFLOW_NAME, description=WORKFLOW_DESCRIPTION)

    def action(self, extra=None):
        self._spawn_shell_and_quit()
        self.os_command_list = self._load_os_command_list()

    """ PRIVATE """

    def _spawn_shell_and_quit(self):
        p = subprocess.Popen(self._determine_os_shell_command(), shell=True)
        sleep(5)
        p.kill()


    def _determine_os_shell_command(self):
        return self._get_random_os_command()


    def _get_random_os_command(self):
        return random.choice(self.os_command_list)

    @staticmethod
    def _load_os_command_list():
        os_command = []
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'os_commands.txt')), 'r') as f:
            for line in f:
                os_command.append(line)
        return os_command

if __name__=='__main__':
    try:
        ShellTest=SpawnShell()
        ShellTest.action()
    except Exception as err:
        print(repr(err))