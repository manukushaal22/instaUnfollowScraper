from selenium import webdriver
from helpers import props, instapy

if __name__=="__main__":
    properties = props.Properties()
    driver = webdriver.Chrome(properties.chrome_driver_path)
    instagram = instapy.Instagram(driver)

    instagram.load_homepage()
    instagram.user_login(properties.insta_username, properties.insta_password)
    instagram.load_profile_page(properties.insta_profile_to_scrape)
    profile_followers = instagram.fetch_followers_list(properties.insta_profile_to_scrape)
    profile_followings = instagram.fetch_followings_list(properties.insta_profile_to_scrape)

    #do whatever you want with the lists
    print(*list(profile_followings-profile_followers))