from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from pathlib import Path
import time


class FolderPage:

    def __init__(self, driver):
        self.driver = driver
        self.account_name = ".folderLink-breadcrumbs"
        self.download_button = "button.is-type-folder"
        self.sort_button = ".sort-dropdown"
        self.size_sort = "li[data-sort='size']"
        self.asc_sort = "li[data-order='ASC']"
        self.dsc_sort = "li[data-order='DESC']"
        self.file_name = ".name-wrp"
        self.file_size = "li.file-size"
        self.loading = ".preloader"
        self.gallery_button = "button[data-mode='gallery']"
        self.gallery_item = ".gallery-item-accessible"
        self.gallery_empty_info = ".gallery-empty-label"

    def get_account_name(self):
        return self.driver.find_element_by_css_selector(self.account_name).text

    def wait_for_account_name(self):
        wait = WebDriverWait(self.driver, 10, 0.01, NoSuchElementException)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.account_name)))

    def download(self):
        wait = WebDriverWait(self.driver, 10, 0.01, NoSuchElementException)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.download_button)))
        self.driver.find_element_by_css_selector(self.download_button).click()
        while self.driver.find_element_by_css_selector(self.download_button).text == "Preparing Download":
            time.sleep(0.5)

    def is_download_finished(self, temp_folder):
        chrome_temp_file = sorted(Path(temp_folder).glob('*.zip.crdownload'))
        downloaded_files = sorted(Path(temp_folder).glob('*.*'))
        if (len(chrome_temp_file) == 0) and (len(downloaded_files) >= 1):
            return True
        else:
            return False

    def wait_for_download(self):
        while self.is_download_finished("../download_test") == False:
            time.sleep(0.5)

    def sort_by_size_asc(self):
        wait = WebDriverWait(self.driver, 2, 0.001, NoSuchElementException)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.sort_button)))
        self.driver.find_element_by_css_selector(self.sort_button).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.size_sort)))
        self.driver.find_element_by_css_selector(self.size_sort).click()
        self.driver.find_element_by_css_selector(self.sort_button).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.asc_sort)))
        self.driver.find_element_by_css_selector(self.asc_sort).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.loading)))
        wait.until(expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, self.loading)))

    def sort_by_size_dsc(self):
        wait = WebDriverWait(self.driver, 2, 0.001, NoSuchElementException)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.sort_button)))
        self.driver.find_element_by_css_selector(self.sort_button).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.size_sort)))
        self.driver.find_element_by_css_selector(self.size_sort).click()
        self.driver.find_element_by_css_selector(self.sort_button).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.dsc_sort)))
        self.driver.find_element_by_css_selector(self.dsc_sort).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.loading)))
        wait.until(expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, self.loading)))

    def get_files_size_asc(self):
        wait = WebDriverWait(self.driver, 10, 0.01, NoSuchElementException)
        wait.until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, self.file_size)))
        sizes = self.driver.find_elements_by_css_selector(self.file_size)
        for i in range(0, len(sizes)):
            sizes[i] = sizes[i].text.split(" ")
            if sizes[i][1] == "B":
                sizes[i] = float(sizes[i][0])
            elif sizes[i][1] == "KB":
                sizes[i] = float(sizes[i][0])*1000
            elif sizes[i][1] == "MB":
                sizes[i] = float(sizes[i][0])*1000000
        return sizes

    def get_files_size_dsc(self):
        wait = WebDriverWait(self.driver, 10, 0.01, NoSuchElementException)
        wait.until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, self.file_size)))
        sizes = self.driver.find_elements_by_css_selector(self.file_size)
        for i in range(0, len(sizes)):
            sizes[i] = sizes[i].text.split(" ")
            if sizes[i][1] == "B":
                sizes[i] = float(sizes[i][0])
            elif sizes[i][1] == "KB":
                sizes[i] = float(sizes[i][0])*1000
            elif sizes[i][1] == "MB":
                sizes[i] = float(sizes[i][0])*1000000
        return sizes

    def check_if_list_sorted_asc(self):
        size_list = self.get_files_size_asc()
        for i in range(1, len(size_list)):
            assert size_list[i] >= size_list[i-1]

    def check_if_list_sorted_dsc(self):
        size_list = self.get_files_size_dsc()
        for i in range(1, len(size_list)):
            assert size_list[i] <= size_list[i-1]

    def how_many_image_files(self):
        wait = WebDriverWait(self.driver, 10, 0.01, NoSuchElementException)
        wait.until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, self.file_name)))
        list_of_files = self.driver.find_elements_by_css_selector(self.file_name)
        amount = 0
        list_of_formats = ["bmp", "jpg", "jpeg", "png", "gif"]
        for element in list_of_files:
            file_format = element.text.split(".")[1]
            for format in list_of_formats:
                if format == file_format:
                    amount += 1
        return amount

    def images_in_gallery_view(self):
        wait = WebDriverWait(self.driver, 2, 0.1, NoSuchElementException)
        self.driver.find_element_by_css_selector(self.gallery_button).click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.loading)))
        wait.until(expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, self.loading)))
        return len(self.driver.find_elements_by_css_selector(self.gallery_item))

    def get_gallery_empty_text(self):
        wait = WebDriverWait(self.driver, 2, 0.1, NoSuchElementException)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.gallery_empty_info)))
        return self.driver.find_element_by_css_selector(self.gallery_empty_info).text
