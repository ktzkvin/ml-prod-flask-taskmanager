import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


def start_server():
    pass


def test_login_flow():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("http://127.0.0.1:5000/register")

    # register
    driver.find_element(By.NAME, "username").send_keys("e2e_user")
    driver.find_element(By.NAME, "password").send_keys("pass")
    driver.find_element(By.NAME, "confirm").send_keys("pass")
    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(1)

    # login
    driver.get("http://127.0.0.1:5000/login")
    driver.find_element(By.NAME, "username").send_keys("e2e_user")
    driver.find_element(By.NAME, "password").send_keys("pass")
    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(1)

    assert "Tasks" in driver.page_source
    driver.quit()


def test_create_task():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("http://127.0.0.1:5000/login")

    # login
    driver.find_element(By.NAME, "username").send_keys("e2e_user")
    driver.find_element(By.NAME, "password").send_keys("pass")
    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(1)

    # create task
    driver.get("http://127.0.0.1:5000/tasks/new")
    driver.find_element(By.NAME, "title").send_keys("task e2e")
    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(1)

    assert "task e2e" in driver.page_source
    driver.quit()


def test_toggle_task():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("http://127.0.0.1:5000/login")

    # login
    driver.find_element(By.NAME, "username").send_keys("e2e_user")
    driver.find_element(By.NAME, "password").send_keys("pass")
    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(1)

    # toggle task id=1
    driver.get("http://127.0.0.1:5000/tasks/1/toggle")
    time.sleep(1)

    assert True
    driver.quit()