from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class SeleniumScraper:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--window-size=1920,1200")

        self.driver = webdriver.Chrome(
            options=self.options, executable_path="chromedriver.exe"
        )

    def __get_fixtures_lines(self, url: str) -> list[str]:
        self.driver.get(url)
        table_web_element = self.driver.find_element(By.ID, "schedule")
        table_text = table_web_element.text

        return table_text.split("\n")

    def scrape_fixtures(self, url: str) -> list[str]:
        return self.__get_fixtures_lines(url)

    def __get_statistics_lines(self, url: str) -> list[str]:
        self.driver.get(url)
        table_web_element = self.driver.find_element(By.ID, "team_and_opponent")
        table_text = table_web_element.text

        return table_text.split("\n")

    def scrape_statistics(self, url: str) -> list[str]:
        return self.__get_statistics_lines(url)
