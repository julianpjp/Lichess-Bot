from selenium.webdriver.common.keys import Keys
from listener import Listener
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class Login():

    def login(self, email, password, color, timePerMove, modus):
        self.email = email
        self.password = password 
        self.color = color 
        self.timPerMove = timePerMove
        self.modus = modus

        self.driver = webdriver.Chrome(options=self.setOptions())
        self.driver.get('https://lichess.org/login')


        email_input = self.driver.find_element_by_id('form3-username')
        email_input.send_keys(email)
        password_input = self.driver.find_element_by_id('form3-password')
        password_input.send_keys(password)
        time.sleep(1)
        password_input.send_keys(Keys.ENTER)

        return

    def setOptions(self):
        # returns the options for chromedriver 
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1280,800")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
        return options