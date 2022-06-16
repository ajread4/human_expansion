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

    def action(self, extra=None):
        self._run_user_and_quit()

    """ PRIVATE """

    def _run_user_and_quit(self):
        p = subprocess.Popen("cmd.exe /C echo " + self._determine_echo_shell_command(), shell=True)
        sleep(5)
        p.kill()

