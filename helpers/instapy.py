from selenium.webdriver.common.keys import Keys
import time
from . import logpy

class Instagram:
    def __init__(self, driver):
        self.driver = driver
        self.username_element_name = "username"
        self.password_element_name = "password"
        self.login_button_xpath = "//button[@type='submit']"
        self.homepage_url = "https://www.instagram.com/"


    def load_homepage(self, wait_time = 3):
        logpy.info("loading homepage...")
        self.driver.get(self.homepage_url)
        time.sleep(wait_time)
        logpy.info("loaded homepage!")

    def load_profile_page(self,profile_id, wait_time = 3):
        logpy.info("loading profile page...")
        self.driver.get(self.homepage_url+profile_id)
        time.sleep(wait_time)
        logpy.info("loaded profile page!")

    def user_login(self, username, password, wait_time = 3):
        logpy.info("logging in user...")
        self.driver.find_element_by_name(self.username_element_name).send_keys(username)
        self.driver.find_element_by_name(self.password_element_name).send_keys(password)
        time.sleep(wait_time)
        self.driver.find_element_by_xpath(self.login_button_xpath).send_keys(Keys.ENTER)
        time.sleep(wait_time)
        logpy.info("user logged in!")

    def get_into_classes(self, element, class_list):
        temp = element
        for class_name in class_list:
            temp = temp.find_element_by_class_name(class_name)
        return temp

    def scroll_down_to_last(self):
        logpy.info("start scrolling...")
        scrollable_div_class_name = "isgrP"
        last_height = self.driver.execute_script("return document.body.getElementsByClassName('"+scrollable_div_class_name+"')[0].scrollHeight")
        while True:
            logpy.info("command scroll")
            self.driver.execute_script("document.body.getElementsByClassName('"+scrollable_div_class_name+"')[0].scrollTo(0, document.body.getElementsByClassName('"+scrollable_div_class_name+"')[0].scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.getElementsByClassName('"+scrollable_div_class_name+"')[0].scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        logpy.info("scrolled to end")

    def extract_list(self):
        self.scroll_down_to_last()
        follower_element_list = self.driver.find_elements_by_class_name("wo9IH")
        # class_list = ["uu6c_", "t2ksc", "enpQJ", "d7ByH"]
        follower_names = set()
        for follower_element in follower_element_list:
            follower_names.add(follower_element.text.split('\n')[0])
        return follower_names

    def fetch_followers_list(self, username, wait_time = 1):
        self.load_profile_page(username)
        logpy.info("fetching followers...")
        self.driver.find_element_by_partial_link_text("followers").click()
        time.sleep(wait_time)
        logpy.info("followers extracted successfully!")
        return self.extract_list()

    def fetch_followings_list(self, username, wait_time = 1):
        self.load_profile_page(username)
        logpy.info("fetching followings...")
        self.driver.find_element_by_partial_link_text("following").click()
        time.sleep(wait_time)
        logpy.info("followings extracted successfully!")
        return self.extract_list()