import pytest
from selenium import webdriver
from page_object_pattern.pages.login import LoginPage
from page_object_pattern.pages.folder_page import FolderPage


class TestLogin:

    @pytest.fixture()
    def setup(self):
        self.driver = webdriver.Chrome()
        yield
        self.driver.quit()

    def test_failed_login(self, setup):
        self.driver.get("https://qarecruitment.egnyte.com/fl/5f1vF0Psut")
        login_page = LoginPage(self.driver)
        login_page.enter_password("h0wdY7Vcmp")
        login_page.click_continue()
        login_page.wait_for_error_info()
        assert login_page.get_error_info() == "Incorrect password. Try again."

    def test_login(self, setup):
        self.driver.get("https://qarecruitment.egnyte.com/fl/5f1vF0Psut")
        login_page = LoginPage(self.driver)
        folder_page = FolderPage(self.driver)
        login_page.enter_password("7ck3uq97")
        login_page.click_continue()
        folder_page.wait_for_account_name()
        assert folder_page.get_account_name() == "Michał Goryński"
