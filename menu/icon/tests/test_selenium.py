from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys



class Hosttest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:8000/")
    
    def test_home_title(self):
        self.assertIn("Page", self.driver.title  )
        self.driver.quit()


    def test_gotten_class_name_correct(self):

        category = self.driver.find_element_by_id("category_title")  
        self.assertEquals(category.text, "Categories")
        self.driver.quit()


    # def test_log_in(self):
    #     self.driver = webdriver.Firefox()

    #     self.driver.get("http://127.0.0.1:8000/sign_in/")
        

    #     username = self.driver.find_element_by_name("username")
    #     password = self.driver.find_element_by_name("password")
    #     submit = self.driver.find_element_by_name("submit_button")

    #     username.send_keys("Admin") 
    #     password.send_keys("admin")
    #     submit.send_keys(Keys.RETURN)

    #     try:
    #         # self.driver.get("http://127.0.0.1:8000/accounts/profile/")
    #         self.assertEquals(self.driver.title, "Profile")

    #     except:
    #         self.driver.quit()

    