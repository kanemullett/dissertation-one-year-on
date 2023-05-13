from selenium_scraper import SeleniumScraper
import pandas as pd


class SeasonStatistics:
    def __init__(self, team_abbreviation: str, year: str):
        self.__team_abbreviation = team_abbreviation
        self.__year = year

        self.__statistics = self.__generate_statistics()

        self.__headings = self.__create_headings()

        self.__team_statistics = self.__create_team_statistics()
        self.__opponent_statistics = self.__create_opponent_statistics()

        self.__team_statistics_dataframe = pd.DataFrame(columns=self.__headings)
        self.__opponent_statistics_dataframe = pd.DataFrame(columns=self.__headings)

    def get_team_dataframe(self) -> pd.DataFrame:
        self.__populate_team_dataframe()

        return self.__team_statistics_dataframe

    def get_opponent_dataframe(self) -> pd.DataFrame:
        self.__populate_opponent_dataframe()

        return self.__opponent_statistics_dataframe

    def __generate_statistics(self) -> list[str]:
        this_scraper = SeleniumScraper()
        statistics = this_scraper.scrape_statistics(
            f"https://www.basketball-reference.com/teams/"
            f"{self.__team_abbreviation}/{self.__year}.html#all_team_and_opponent"
        )
        this_scraper.driver.quit()

        return statistics

    def __create_headings(self) -> list[str]:
        heading_row = self.__statistics[0]
        headings = heading_row.split()

        return headings

    def __create_team_statistics(self) -> list[str]:
        team_statistics_row = self.__statistics[1]
        team_statistics = team_statistics_row.split()
        team_statistics.pop(0)

        return self.__format_decimals(team_statistics)

    def __create_opponent_statistics(self) -> list[str]:
        opponent_statistics_row = self.__statistics[5]
        opponent_statistics = opponent_statistics_row.split()
        opponent_statistics.pop(0)

        return self.__format_decimals(opponent_statistics)

    @staticmethod
    def __format_decimals(statistics: list[str]) -> list[str]:
        formatted_statistics = []

        for statistic in statistics:
            if statistic[0] == ".":
                statistic = "0" + statistic
            formatted_statistics.append(statistic)

        return formatted_statistics

    def __populate_team_dataframe(self):
        self.__team_statistics_dataframe.loc[
            len(self.__team_statistics_dataframe)
        ] = self.__to_dataframe_row(self.__team_statistics)

    def __populate_opponent_dataframe(self):
        self.__opponent_statistics_dataframe.loc[
            len(self.__opponent_statistics_dataframe)
        ] = self.__to_dataframe_row(self.__opponent_statistics)

    @staticmethod
    def __to_dataframe_row(statistics: list[str]) -> dict[str, str]:
        return {
            "G": statistics[0],
            "MP": statistics[1],
            "FG": statistics[2],
            "FGA": statistics[3],
            "FG%": statistics[4],
            "3P": statistics[5],
            "3PA": statistics[6],
            "3P%": statistics[7],
            "2P": statistics[8],
            "2PA": statistics[9],
            "2P%": statistics[10],
            "FT": statistics[11],
            "FTA": statistics[12],
            "FT%": statistics[13],
            "ORB": statistics[14],
            "DRB": statistics[15],
            "TRB": statistics[16],
            "AST": statistics[17],
            "STL": statistics[18],
            "BLK": statistics[19],
            "TOV": statistics[20],
            "PF": statistics[21],
            "PTS": statistics[22],
        }
