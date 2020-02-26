from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.password_input = "input#password"
        self.continue_button = ".primaryBtn"
        self.error_info = "div.error"
        self.accept_button = "button[data-role='accept-consent']"

    def enter_password(self, password):
        self.driver.find_element_by_css_selector(self.password_input).send_keys(password)

    def click_continue(self):
        self.driver.find_element_by_css_selector(self.continue_button).click()

    def wait_for_error_info(self):
        wait = WebDriverWait(self.driver, 10, 0.1, NoSuchElementException)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.error_info)))

    def get_error_info(self):
        return self.driver.find_element_by_css_selector(self.error_info).text
