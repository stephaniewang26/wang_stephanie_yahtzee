import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 

import random

class Save_Load_UI_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

    def test_save_incomplete_game(self): 
        self.browser.get(self.url)

        self.assertTrue(False) #0: blank.svg         
            
        print("_ passed")
    
    def test_only_save_scores_for_disabled_categories(self): 
        self.browser.get(self.url)

        self.assertTrue(False) #0: blank.svg         
            
        print("_ passed")
    
    def test_load_and_disable_categories(self): 
        self.browser.get(self.url)

        self.assertTrue(False) #0: blank.svg         
            
        print("_ passed")
    
    def test_no_error_with_load_nonexistent_game(self): 
        self.browser.get(self.url)

        self.assertTrue(False) #0: blank.svg         
            
        print("_ passed")

if __name__ == '__main__':
    unittest.main()