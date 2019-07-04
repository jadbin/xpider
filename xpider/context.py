# coding=utf-8

import json

from selenium.webdriver import Chrome, ChromeOptions

from xpider.utils import add_script_to_evaluate_on_new_document


class DefaultContext:
    def __init__(self):
        self.chrome_arguments = [
            '--headless',
            '--incognito',
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--disable-popup-blocking',
            '--disable-gpu',
            '--no-sandbox'
        ]
        self.chrome_experimental_options = {
            'prefs': {
                'profile.managed_default_content_settings.images': 2
            }
        }
        self.cookies = []
        self.local_storage = {}
        self.session_storage = {}
        self.timeout = 20

    def create_web_driver(self):
        driver = Chrome(options=self.make_chrome_options())
        driver.set_page_load_timeout(self.timeout)
        driver.set_script_timeout(self.timeout)
        driver.implicitly_wait(self.timeout)
        if self.cookies:
            for c in self.cookies:
                driver.add_cookie(c)
        if self.local_storage:
            for k, v in self.local_storage.items():
                add_script_to_evaluate_on_new_document(
                    'localStorage.setItem("{}", "{}");'.format(k.replace('"', r'\"'), v.replace('"', r'\"')), driver)
        if self.session_storage:
            for k, v in self.session_storage.items():
                add_script_to_evaluate_on_new_document(
                    'sessionStorage.setItem("{}", "{}");'.format(k.replace('"', r'\"'), v.replace('"', r'\"')), driver)
        return driver

    def make_chrome_options(self):
        chrome_options = ChromeOptions()
        for arg in self.chrome_arguments:
            chrome_options.add_argument(arg)
        for k, v in self.chrome_experimental_options.items():
            chrome_options.add_experimental_option(k, v)
        return chrome_options

    def update_cookies(self, driver):
        self.cookies = driver.get_cookies()

    def update_local_storage(self, driver):
        self.local_storage = json.loads(driver.execute_script('return JSON.stringfy(localStorage);'))

    def update_session_storage(self, driver):
        self.session_storage = json.loads(driver.execute_script('return JSON.stringfy(sessionStorage);'))


class MobileContext(DefaultContext):
    def __init__(self):
        super().__init__()
        self.chrome_experimental_options['mobileEmulation'] = {'deviceName': 'iPhone 8'}
