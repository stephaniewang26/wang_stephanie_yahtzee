import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 

import random

class Feedback_UI_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

    def test_load_nonexistent_game_bad(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")

    def test_enter_invalid_score_bad(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")
    
    def test_roll_too_many_times_bad(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")
    
    def test_enter_score_with_blank_dice_bad(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")

    def test_enter_valid_score_good(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")  

    def test_new_game_good(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed") 

    def test_successful_save_good(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")   

    def test_successful_load_good(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")   
    
    def test_finish_game_good(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")  

    def test_feedback_cleared_with_new_roll(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")    

if __name__ == '__main__':
    unittest.main()