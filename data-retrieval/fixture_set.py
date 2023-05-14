from selenium_scraper import SeleniumScraper
import pandas as pd


class FixtureSet:
    """
    Fixture Set object for a month of NBA games.

    :param month: The month of the fixtures.
    :type month: str
    :param year: The season within which the fixtures are played.
    :type year: str
    """

    def __init__(self, month: str, year: str):
        self.__month = month
        self.__year = year

        self.__fixtures = self.__generate_fixtures()

        self.__headings = self.__create_headings()

        self.__dataframe = pd.DataFrame(columns=self.__headings)

    def get_dataframe(self) -> pd.DataFrame:
        """
        Retrieve a dataframe populated with the fixtures for the given timespan.

        :return: The fixtures dataframe.
        :rtype: DataFrame
        """

        self.__populate_dataframe()

        return self.__dataframe

    def __generate_fixtures(self) -> list[str]:
        """
        Generate fixtures by scraping a Basketball-Reference table.

        :return: Lines of a fixtures table.
        :rtype: list[str]
        """

        this_scraper = SeleniumScraper()
        fixtures = this_scraper.scrape_fixtures(
            f"https://www.basketball-reference.com/leagues/NBA_{self.__year}_games-{self.__month}.html"
        )
        this_scraper.driver.quit()

        return fixtures

    def __create_headings(self) -> list[str]:
        """
        Create a list of headings from the lines of a fixtures table.

        :return: List of headings.
        :rtype: list[str]
        """

        heading_row = self.__fixtures[0]
        condensed_headings = self.__remove_unnecessary_headings(heading_row.split())

        return self.__revise_heading_names(condensed_headings)

    @staticmethod
    def __remove_unnecessary_headings(headings: list[str]) -> list[str]:
        """
        Clean a list of headings to remove unnecessary headings.

        :param headings: List of headings.
        :type headings: list[str]
        :return: Cleaned list of headings with unnecessary headings removed.
        :rtype: list[str]
        """

        return [
            heading
            for heading in headings
            if heading != "(ET)" and heading != "Notes" and heading != "Arena"
        ]

    @staticmethod
    def __revise_heading_names(headings: list[str]) -> list[str]:
        """
        Rename some headings to more appropriate or legible names.

        :param headings: List of headings.
        :type headings: list[str]
        :return: List of more appropriately named headings.
        :rtype: list[str]
        """

        if headings[1] == "Start":
            headings[1] = "Tip-Off Time"

        if headings[2] == "Visitor/Neutral":
            headings[2] = "Away Team"

        if headings[3] == "PTS":
            headings[3] = "Away PTS"

        if headings[4] == "Home/Neutral":
            headings[4] = "Home Team"

        if headings[5] == "PTS":
            headings[5] = "Home PTS"

        if headings[6] == "Attend.":
            headings[6] = "Attendance"

        return headings

    @staticmethod
    def __create_row(fixture: str) -> dict[str, str]:
        """
        Convert a line of fixture data to a fixture dictionary which can then be appended as a row to a dataframe.

        :param fixture: Line of fixture data.
        :type fixture: str
        :return: Fixture dictionary.
        :rtype: dict[str, str]
        """

        split_row = fixture.split()

        split_row = [value for value in split_row if value != "OT" and value != "(IV)"]

        three_names = ["Los", "Golden", "New", "Oklahoma", "Portland", "San"]

        date_field = f"{split_row[1]} {split_row[2]} {split_row[3]}"
        time_field = f"{split_row[4]}"
        away_team_field = f"{split_row[5]} {split_row[6]}"
        away_points_field = f"{split_row[7]}"
        home_team_field = f"{split_row[8]} {split_row[9]}"
        home_points_field = f"{split_row[10]}"
        attendance_field = f"{split_row[13]}"

        if len(split_row) == 19:
            away_team_field = f"{split_row[5]} {split_row[6]} {split_row[7]}"
            away_points_field = f"{split_row[8]}"
            home_team_field = f"{split_row[9]} {split_row[10]} {split_row[11]}"
            home_points_field = f"{split_row[12]}"
            attendance_field = f"{split_row[15]}"

        elif len(split_row) == 18 and split_row[5] in three_names:
            away_team_field = f"{split_row[5]} {split_row[6]} {split_row[7]}"
            away_points_field = f"{split_row[8]}"
            if split_row[9] in three_names:
                home_team_field = f"{split_row[9]} {split_row[10]} {split_row[11]}"
                home_points_field = f"{split_row[12]}"
                attendance_field = f"{split_row[15]}"
            else:
                home_team_field = f"{split_row[9]} {split_row[10]}"
                home_points_field = f"{split_row[11]}"
                attendance_field = f"{split_row[14]}"

        elif len(split_row) == 18 and split_row[5] not in three_names:
            away_team_field = f"{split_row[5]} {split_row[6]}"
            away_points_field = f"{split_row[7]}"
            home_team_field = f"{split_row[8]} {split_row[9]} {split_row[10]}"
            home_points_field = f"{split_row[11]}"
            attendance_field = f"{split_row[14]}"

        elif len(split_row) == 17 and split_row[5] in three_names:
            away_team_field = f"{split_row[5]} {split_row[6]} {split_row[7]}"
            away_points_field = f"{split_row[8]}"
            home_team_field = f"{split_row[9]} {split_row[10]}"
            home_points_field = f"{split_row[11]}"
            attendance_field = f"{split_row[14]}"

        elif len(split_row) == 17 and split_row[5] not in three_names:
            away_team_field = f"{split_row[5]} {split_row[6]}"
            away_points_field = f"{split_row[7]}"
            if split_row[8] in three_names:
                home_team_field = f"{split_row[8]} {split_row[9]} {split_row[10]}"
                home_points_field = f"{split_row[11]}"
                attendance_field = f"{split_row[14]}"
            else:
                home_team_field = f"{split_row[8]} {split_row[9]}"
                home_points_field = f"{split_row[10]}"
                attendance_field = f"{split_row[13]}"

        return {
            "Date": date_field,
            "Tip-Off Time": time_field,
            "Away Team": away_team_field,
            "Away PTS": away_points_field,
            "Home Team": home_team_field,
            "Home PTS": home_points_field,
            "Attendance": attendance_field,
        }

    def __populate_dataframe(self) -> None:
        """
        Populate the fixtures dataframe with the rows of fixtures.
        """

        data = self.__fixtures
        data.pop(0)

        for row in data:
            if row[0:4] != "Date":
                self.__dataframe.loc[len(self.__dataframe)] = self.__create_row(row)


if __name__ == "__main__":
    hello = FixtureSet("october", "2023")
    print(hello.get_dataframe()["Date"][0])
