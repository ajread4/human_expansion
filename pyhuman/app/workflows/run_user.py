import subprocess
import sys
from time import sleep
import os
import random
from pathlib import Path, PureWindowsPath

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
        self.root_path=PureWindowsPath("C:\\Users\\cptadmin\\Documents\\")
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
            print(f'Creating file named {f} with content {w} in the Documents directory')
            self._write_file(str(self.root_path.joinpath(f)))
            return '\"echo ' + w + ' > ' + str(self.root_path.joinpath(f)) + '\"'
        elif chosen_behavior==2: #Create a directory within documents directory.
            _, d, _ = self._load_behavior()
            print(f'Creating directory named {d} in the Documents directory')
            self._write_dir(str(self.root_path.joinpath(d)))
            return '\"mkdir ' + str(self.root_path.joinpath(d)) + "\""
        elif chosen_behavior==3: #Move a file within documents directory.
            original_file, _, w = self._load_behavior()
            new_file, _, _ = self._load_behavior()
            print(f'Moving file named {original_file} in the Documents directory to {new_file}')
            if not (self._check_file_exist(original_file)):
                make_p = subprocess.Popen("cmd.exe /C \"echo " + w + " > " + str(self.root_path.joinpath(original_file)) + "\"", shell=True)
                sleep(2)
                make_p.kill()
                self._write_file(str(self.root_path.joinpath(original_file)))
            self._write_file(str(self.root_path.joinpath(new_file)))
            return '\"move ' + str(self.root_path.joinpath(original_file)) + ' ' + str(self.root_path.joinpath(new_file)) + "\""
        elif chosen_behavior == 4: #Move a directory within another documents directory.
            _, firstdir, _ = self._load_behavior()
            _, seconddir, _ = self._load_behavior()
            print(f'Moving directory named {firstdir} to {seconddir} in the documents directory')
            if not (self._check_dir_exist(firstdir)):
                make_p = subprocess.Popen("cmd.exe /C \"mkdir " + str(self.root_path.joinpath(firstdir)) + "\"", shell=True)
                sleep(2)
                make_p.kill()
                self._write_dir(str(self.root_path.joinpath(firstdir)))
            self._write_dir(str(self.root_path.join(seconddir)))
            return '\"mkdir ' + str(self.root_path.joinpath(firstdir,seconddir)) + "\""
        elif chosen_behavior == 5: #Delete a file from documents directory.
            if (self._created_files_status()):
                f=self._retrieve_file()
                print(f'Deleting file {f} in Documents')
                return '\"del ' +str(self.root_path.joinpath(f)) + "\""
            else:
                return 'echo Human'
        elif chosen_behavior == 6: #Delete a directory from a directory.
            if (self._created_dir_status()):
                d=self._retrieve_dir()
                print(f'Deleting directory {d} within Documents')
                return '\"rmdir /S ' + str(self.root_path.joinpath(d)) + "\""
            else:
                return 'echo Human'
        elif chosen_behavior == 7: #Modify a file within documents directory
            if (self._created_files_status()):
                f,_,w=self._load_behavior()
                print(f'Modifying file {f} with content {w} in Documents directory')
                if not (self._check_file_exist(f)):
                    make_p = subprocess.Popen("cmd.exe /C \"echo " + w + " > " + str(self.root_path.joinpath(f))+ "\"", shell=True)
                    sleep(2)
                    make_p.kill()
                    self._write_file(str(self.root_path.joinpath(f)))
                return '\"echo ' + w + ' > ' + str(self.root_path.joinpath(f)) + "\""
            else:
                return 'echo Human'
        else: #if there isnt a correct behavior chosen
            print(f'Incorrect chosen behavior: {chosen_behavior}')

    def _get_random_behavior(self):
        #return random.choice(list(self.userbehavior.keys())) #if only want random probabilities for interactions
        return random.choices(list(self.userbehavior.keys()),weights=(30,30,15,5,5,5,10),k=1)[0] #if want weighted probabilities

    def _check_file_exist(self,input_file):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'created_files.txt')), 'r') as f:
            for line in f.readlines():
                if input_file == line.split("\\")[-1]:
                    return True
            return False

    def _check_dir_exist(self,input_dir):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'created_dirs.txt')), 'r') as d:
            for line in d.readlines():
                if input_dir in line.split("\\")[-1]:
                    return True
            return False
    def _write_file(self,input_file):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'created_files.txt')), 'a') as f:
            f.write(input_file + "\n")

    def _write_dir(self,input_dir):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'created_dirs.txt')), 'a') as d:
            d.write(input_dir + "\n")
    @staticmethod
    def _load_behavior():
        random_file=random.choice(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', 'file_options.txt')), 'r').read().splitlines())
        random_dir = random.choice(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', 'dir_options.txt')), 'r').read().splitlines())
        random_words=random.choice(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', 'echo_words.txt')), 'r').read().splitlines())
        return random_file,random_dir,random_words

    @staticmethod
    def _created_files_status():
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'created_files.txt')), 'r') as f:
            if len(f.readlines())==0:
                return False
            else:
                return True

    @staticmethod
    def _created_dir_status():
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'created_dirs.txt')), 'r') as d:
            if len(d.readlines())==0:
                return False
            else:
                return True
    @staticmethod
    def _retrieve_dir():
        return random.choice(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', 'created_dirs.txt')), 'r').read().splitlines())

    @staticmethod
    def _retrieve_file():
        return random.choice(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', 'created_files.txt')), 'r').read().splitlines())