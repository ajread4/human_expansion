import subprocess
import sys
from time import sleep
import os
import random

from ..utility.base_workflow import BaseWorkflow


WORKFLOW_NAME = 'Run Echo Commands'
WORKFLOW_DESCRIPTION = 'Run random echo commands within cmd.exe to emulate a user'


def load():
    return RunEcho()


class RunEcho(BaseWorkflow):

    def __init__(self):
        super().__init__(name=WORKFLOW_NAME, description=WORKFLOW_DESCRIPTION)
        self.echo_command_list = self._load_echo_command_list()

    def action(self, extra=None):
        self._spawn_echo_and_quit()

    """ PRIVATE """

    def _spawn_echo_and_quit(self):
        p = subprocess.Popen("cmd.exe /C echo " + self._determine_echo_shell_command(), shell=True)
        sleep(5)
        p.kill()


    def _determine_echo_shell_command(self):
        return self._get_random_echo_command()


    def _get_random_echo_command(self):
        return random.choice(self.echo_command_list)

    @staticmethod
    def _load_echo_command_list():
        echo_command = []
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'echo_words.txt')), 'r') as f:
            for line in f:
                echo_command.append(line)
        return echo_command

