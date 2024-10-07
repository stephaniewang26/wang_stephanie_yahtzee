import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 

import random

class Gameplay_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

    def test_player_allowed_3_rolls_max(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")
    
    def test_player_must_enter_score_even_0(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")
    
    def test_prevent_entry_invalid_scores(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")
    
    def test_prevent_dice_rolls_for_finished_games(self): 
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")
    
    def test_dice_reset_after_valid_score(self): 
        # blank and unreserved
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")
    
    def test_new_game_blank_totals_and_categories(self): 
        # blank and unreserved
        self.browser.get(self.url)

        self.assertTrue(False)         
            
        print("_ passed")


if __name__ == '__main__':
    unittest.main()