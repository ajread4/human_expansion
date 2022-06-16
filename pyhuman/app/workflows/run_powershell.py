os_commands.txtimport subprocess
import sys
from time import sleep
import os
import random

from ..utility.base_workflow import BaseWorkflow


WORKFLOW_NAME = 'Run Powershell Commands'
WORKFLOW_DESCRIPTION = 'Run random powershell commands to emulate a user'


def load():
    return RunPowerShell()


class RunPowerShell(BaseWorkflow):

    def __init__(self):
        super().__init__(name=WORKFLOW_NAME, description=WORKFLOW_DESCRIPTION)
        self.ps_command_list = self._load_ps_command_list()

    def action(self, extra=None):
        self._spawn_ps_and_quit()

    """ PRIVATE """

    def _spawn_ps_and_quit(self):
        p = subprocess.Popen("powershell.exe " + self._determine_ps_command(), shell=True)
        sleep(5)
        p.kill()


    def _determine_ps_command(self):
        return self._get_random_ps_command()


    def _get_random_ps_command(self):
        return random.choice(self.ps_command_list)

    @staticmethod
    def _load_ps_command_list():
        ps_command = []
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'powershell_commands.txt')), 'r') as f:
            for line in f:
                ps_command.append(line)
        return ps_command

