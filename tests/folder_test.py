import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from page_object_pattern.pages.login import LoginPage
from page_object_pattern.pages.folder_page import FolderPage
import os
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {"download.default_directory": "/Users/michalgorynski/PycharmProjects/Egnyte_test/download_test"})


class TestFolder:

    @pytest.fixture()
    def setup(self):
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        yield
        self.driver.quit()

    def test_download_folder(self, setup):
        path_to_file = '../download_test/Michał Goryński.zip'
        self.driver.get("https://qarecruitment.egnyte.com/fl/5f1vF0Psut")
        login_page = LoginPage(self.driver)
        folder_page = FolderPage(self.driver)
        login_page.enter_password("7ck3uq97")
        login_page.click_continue()
        folder_page.wait_for_account_name()
        folder_page.download()
        folder_page.wait_for_download()
        assert os.path.isfile(path_to_file) == True
        os.remove(path_to_file)

    def test_sorting_by_size(self, setup):
        self.driver.get("https://qarecruitment.egnyte.com/fl/5f1vF0Psut")
        login_page = LoginPage(self.driver)
        folder_page = FolderPage(self.driver)
        login_page.enter_password("7ck3uq97")
        login_page.click_continue()
        self.driver.get("https://qarecruitment.egnyte.com/fl/5f1vF0Psut#folder-link/Micha%C5%82%20Gory%C5%84ski/DataFolder1/testData")
        folder_page.sort_by_size_asc()
        folder_page.check_if_list_sorted_asc()
        folder_page.sort_by_size_dsc()
        folder_page.check_if_list_sorted_dsc()

    def test_gallery_view(self, setup):
        self.driver.get("https://qarecruitment.egnyte.com/fl/5f1vF0Psut")
        login_page = LoginPage(self.driver)
        folder_page = FolderPage(self.driver)
        login_page.enter_password("7ck3uq97")
        login_page.click_continue()
        self.driver.get("https://qarecruitment.egnyte.com/fl/5f1vF0Psut#folder-link/Micha%C5%82%20Gory%C5%84ski/DataFolder1/testData")
        assert folder_page.how_many_image_files() == folder_page.images_in_gallery_view()
        self.driver.get("https://qarecruitment.egnyte.com/fl/5f1vF0Psut#folder-link/Micha%C5%82%20Gory%C5%84ski/DataFolder1/numbers")
        assert folder_page.how_many_image_files() == folder_page.images_in_gallery_view()
        assert folder_page.get_gallery_empty_text() == "There are no images to show in this folder"
