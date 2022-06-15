import subprocess
import sys
from time import sleep
import os
import random

from ..utility.base_workflow import BaseWorkflow


WORKFLOW_NAME = 'Run OS Commands'
WORKFLOW_DESCRIPTION = 'Run random OS commands within cmd.exe to emulate a user'


def load():
    return RunOS()


class RunOS(BaseWorkflow):

    def __init__(self):
        super().__init__(name=WORKFLOW_NAME, description=WORKFLOW_DESCRIPTION)
        self.os_command_list = self._load_os_command_list()

    def action(self, extra=None):
        self._spawn_cmd_and_quit()

    """ PRIVATE """

    def _spawn_cmd_and_quit(self):
        p = subprocess.Popen("cmd.exe /C " + self._determine_os_shell_command(), shell=True)
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

