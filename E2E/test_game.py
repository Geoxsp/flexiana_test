from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

driver = webdriver.Chrome()


def test_access_website():
    driver.get("https://www.gamesforthebrain.com/game/checkers/")
    sleep(2)
    assert driver.current_url == "https://www.gamesforthebrain.com/game/checkers/"


def test_accept_cookies():
    driver.find_element(By.CSS_SELECTOR, ".qc-cmp2-summary-buttons > button:nth-of-type(2)").click()
    sleep(2)
    try:
        driver.find_element(By.CSS_SELECTOR, ".qc-cmp2-consent-info")
        assert False, "Cookies modal still present"
    except NoSuchElementException as e:
        assert True


def test_start_game():
    driver.find_element(By.CSS_SELECTOR, ".footnote > a:nth-of-type(1)").click()
    sleep(1)
    message = driver.find_element(By.CSS_SELECTOR, "p#message").text
    assert message.strip() == "Select an orange piece to move."


# Make your first move
def test_first_move():
    driver.find_element(By.NAME, "space22").click()
    driver.find_element(By.NAME, "space13").click()

    check = driver.find_element(By.NAME, "space13").get_attribute("src")
    assert check == "https://www.gamesforthebrain.com/game/checkers/you2.gif", "Your piece is not in this position"


# Let computer move
def test_computer_move():
    sleep(2)
    check_src = driver.find_element(By.NAME, "space24").get_attribute("src")
    assert check_src == "https://www.gamesforthebrain.com/game/checkers/me1.gif", "Computer is not in this place"


# Make your second move
def test_second_move():
    driver.find_element(By.NAME, "space42").click()
    driver.find_element(By.NAME, "space33").click()

    check_scr = driver.find_element(By.NAME, "space33").get_attribute("src")
    assert check_scr == "https://www.gamesforthebrain.com/game/checkers/you2.gif", "Your piece is not in this position"


# Let computer take your piece
# Make sure your piece is taken
def test_piece_taken():
    sleep(5)
    area = driver.find_element(By.NAME, "space33").get_attribute("src")
    assert area == "https://www.gamesforthebrain.com/game/checkers/gray.gif", "Area not empty"


# Start a new game
def test_restart_game():
    driver.find_element(By.CSS_SELECTOR, ".footnote > a:nth-of-type(1)").click()
    sleep(1)
    message = driver.find_element(By.CSS_SELECTOR, "p#message").text
    assert message.strip() == "Select an orange piece to move."

driver.quit()
