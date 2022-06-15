import os
import random
from time import sleep

from ..utility.base_workflow import BaseWorkflow
from ..utility.webdriver_helper import WebDriverHelper


WORKFLOW_NAME = 'WebBrowser'
WORKFLOW_DESCRIPTION = 'Select a random website and browse'

DEFAULT_INPUT_WAIT_TIME = 2

def load():
    driver = WebDriverHelper()
    return WebBrowse(driver=driver)


class WebBrowse(BaseWorkflow):

    def __init__(self, driver, input_wait_time=DEFAULT_INPUT_WAIT_TIME):
        super().__init__(name=WORKFLOW_NAME, description=WORKFLOW_DESCRIPTION, driver=driver)

        self.input_wait_time = input_wait_time
        self.website_list = self._load_website_list()

    def action(self, extra=None):
        self._web_browse()

    """ PRIVATE """

    def _web_browse(self):
        random_website = self._get_random_website()
        try:
            self.driver.driver.get('https://' + random_website)
            sleep(self.input_wait_time)
        except Exception as e:
            print('Error loading random website %s: %s' % (random_website.rstrip(), e))

    def _get_random_website(self):
        return random.choice(self.website_list)

    @staticmethod
    def _load_website_list():
        wordlist = []
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                               'data', 'websites.txt')), 'r') as f:
            for line in f:
                wordlist.append(line)
        return wordlist
