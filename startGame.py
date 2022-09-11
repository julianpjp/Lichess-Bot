from listener import Listener
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class StartGame():

    def playOnline(self):
        return

    def playAI(self, color, timePerMove):
        # connect to website and choose AI
        driver = webdriver.Chrome(options=self.setOptions())
        driver.get('https://lichess.org/setup/ai')

        # wait till website is loaded and choose color to play
        colorOpt = {
            'black' : 0,
            'white' : 2
        }
        time.sleep(2)
        try:
            # wait for page to load and choose a color
            element_present = EC.presence_of_element_located((By.ID, 'modal-wrap'))
            wait.WebDriverWait(driver, 10).until(element_present)
            parentElement = driver.find_element_by_class_name("color-submits")
            elementList = parentElement.find_elements_by_tag_name("button")
            title = driver.current_url
            elementList[colorOpt.get(color)].click()

            # wait till game started and url changes to call the listener 
            for i in range(9):
                if title != driver.current_url:
                    if color == 'white': white = True
                    else: white = False
                    Listener(driver, timePerMove, white)
                    #GetBoard(driver, white, timePerMove)
                    return
                time.sleep(1)
            print('Game did not load!')
            return

        except TimeoutException:
            print('timout')
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