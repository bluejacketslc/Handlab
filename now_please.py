from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import getpass3, sys, socket, os, re

# boolean to indicate the beginning or the end of the class
_sessStart = False 

#open and login to messier
def handle_ruman():
    browser.get('http://ruman.slc/')

    text_password_ruman = browser.find_element_by_name('password')
    text_password_ruman.send_keys(ruman_password + Keys.RETURN)

    #wait for the error message that may be appears
    try:
        try:
            wait = WebDriverWait(browser, 5)
            wait.until(EC.text_to_be_present_in_element((By.ID, 'error-msg'), ' '))
            err = browser.find_element_by_id('error-msg').get_attribute('innerHTML')
            if err != "":
                print "[Ruman.slc]", err, "Exiting..."
                return False
        except Exception as e:
            pass
        browser.find_element_by_css_selector("body").send_keys(Keys.CONTROL, 'a')
        wait = WebDriverWait(browser, 8)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.computer')))

        for act in action_sets:
            btnComp = browser.find_element_by_css_selector(".computer")
            actionChains.move_to_element(btnComp).context_click().perform()
            browser.find_element_by_css_selector(".context-menu-search input").send_keys(act, Keys.DOWN, Keys.ENTER, Keys.ENTER);
        
    except Exception as e:
        pass

    return True

def handle_messier():
    if _sessStart:
        browser.get('http://messier.slc/')

        text_username = browser.find_element_by_id('user')
        text_username.send_keys(username)
        text_password = browser.find_element_by_id('pass')
        text_password.send_keys(password + Keys.RETURN)

        #wait for the error message that may be appears
        try:
            wait = WebDriverWait(browser, 5)
            wait.until(EC.text_to_be_present_in_element((By.ID, 'msg'), 'not'))
            err = browser.find_element_by_id('msg').get_attribute('innerHTML')
            if err != "":
                print "[Messier]", err + ".", "Exiting..."
                return False
        except:
            pass

        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'announcement-container')))

        browser.get('http://messier.slc/Home.aspx#P=Active%20Job')

        wait = WebDriverWait(browser, 25)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rowHover')))

        task = browser.find_element_by_class_name('Deadline')
        task.click()

        # actionChains.key_down(Keys.CONTROL).key_down(Keys.LEFT_SHIFT).send_keys('j').key_up(Keys.CONTROL).key_up(Keys.LEFT_SHIFT).perform()
        wait = WebDriverWait(browser, 20)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#view_mode_grid')))

        browser.find_element_by_id('view_mode_grid').click()

        return True

if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] != '-sq':
        print "Usage: python2 {} -sq [start|end]_[general|quiz|final]_session.txt [--wakeup]".format(sys.argv[0])
        exit()
    if sys.argv[1] == '-sq':
        try:
            f = open(sys.argv[2], 'r')
            action_sets = [x.strip() for x in f.read().split(',')]
            if len(sys.argv) == 4 and sys.argv[3] == '--wakeup':
                action_sets.insert(0, 'Wake Up')
            if sys.argv[2].split('_')[0] == 'start':
                _sessStart = True
        except Exception as e:
            print e
            exit()

    os.system("cls")

    print "Hi! You're teaching at room", socket.gethostname()[2:5] + "."

    username = raw_input("Username for Messier: ")
    password = getpass3.getpass("Password for Messier: ")
    ruman_password = getpass3.getpass("Password for Ruman.slc: ")

    browser = webdriver.Chrome("chromedriver_win32/chromedriver.exe")
    browser.fullscreen_window()
    actionChains = ActionChains(browser)

    # if not handle_ruman() or not handle_messier():
    #     browser.close()
    #     exit()

    handle_messier()
    
    print "Done. Happy Teaching!"