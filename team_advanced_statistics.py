from season_statistics import SeasonStatistics
import pandas as pd


class TeamAdvancedStatistics:
    """
    Advanced Statistics object for a team's season.

    :param team_abbreviation: The team's three letter abbreviation.
    :type team_abbreviation: str
    :param year: The team's season for which the advanced statistics pertain.
    :type year: str
    """

    def __init__(self, team_abbreviation: str, year: str):
        self.__team_abbreviation = team_abbreviation
        self.__year = year

        self.__team_dataframe, self.__opponent_dataframe = self.__get_dataframes()

        self.__team_statistics = self.__team_dataframe.loc[0]
        self.__opponent_statistics = self.__opponent_dataframe.loc[0]

        self.__games = float(self.__team_statistics["G"])
        self.__minutes = float(self.__team_statistics["MP"])
        self.__field_goals = float(self.__team_statistics["FG"])
        self.__field_goal_attempts = float(self.__team_statistics["FGA"])
        self.__field_goal_percentage = float(self.__team_statistics["FG%"])
        self.__three_point_makes = float(self.__team_statistics["3P"])
        self.__three_point_attempts = float(self.__team_statistics["3PA"])
        self.__three_point_percentage = float(self.__team_statistics["3P%"])
        self.__two_point_makes = float(self.__team_statistics["2P"])
        self.__two_point_attempts = float(self.__team_statistics["2PA"])
        self.__two_point_percentage = float(self.__team_statistics["2P%"])
        self.__free_throws = float(self.__team_statistics["FT"])
        self.__free_throw_attempts = float(self.__team_statistics["FTA"])
        self.__free_throw_percentage = float(self.__team_statistics["FT%"])
        self.__offensive_rebounds = float(self.__team_statistics["ORB"])
        self.__defensive_rebounds = float(self.__team_statistics["DRB"])
        self.__total_rebounds = float(self.__team_statistics["TRB"])
        self.__assists = float(self.__team_statistics["AST"])
        self.__steals = float(self.__team_statistics["STL"])
        self.__blocks = float(self.__team_statistics["BLK"])
        self.__turnovers = float(self.__team_statistics["TOV"])
        self.__personal_fouls = float(self.__team_statistics["PF"])
        self.__points = float(self.__team_statistics["PTS"])

        self.__opponent_games = float(self.__opponent_statistics["G"])
        self.__opponent_minutes = float(self.__opponent_statistics["MP"])
        self.__opponent_field_goals = float(self.__opponent_statistics["FG"])
        self.__opponent_field_goal_attempts = float(self.__opponent_statistics["FGA"])
        self.__opponent_field_goal_percentage = float(self.__opponent_statistics["FG%"])
        self.__opponent_three_point_makes = float(self.__opponent_statistics["3P"])
        self.__opponent_three_point_attempts = float(self.__opponent_statistics["3PA"])
        self.__opponent_three_point_percentage = float(
            self.__opponent_statistics["3P%"]
        )
        self.__opponent_two_point_makes = float(self.__opponent_statistics["2P"])
        self.__opponent_two_point_attempts = float(self.__opponent_statistics["2PA"])
        self.__opponent_two_point_percentage = float(self.__opponent_statistics["2P%"])
        self.__opponent_free_throws = float(self.__opponent_statistics["FT"])
        self.__opponent_free_throw_attempts = float(self.__opponent_statistics["FTA"])
        self.__opponent_free_throw_percentage = float(self.__opponent_statistics["FT%"])
        self.__opponent_offensive_rebounds = float(self.__opponent_statistics["ORB"])
        self.__opponent_defensive_rebounds = float(self.__opponent_statistics["DRB"])
        self.__opponent_total_rebounds = float(self.__opponent_statistics["TRB"])
        self.__opponent_assists = float(self.__opponent_statistics["AST"])
        self.__opponent_steals = float(self.__opponent_statistics["STL"])
        self.__opponent_blocks = float(self.__opponent_statistics["BLK"])
        self.__opponent_turnovers = float(self.__opponent_statistics["TOV"])
        self.__opponent_personal_fouls = float(self.__opponent_statistics["PF"])
        self.__opponent_points = float(self.__opponent_statistics["PTS"])

        self.__headings = [
            "PPG",
            "PAPG",
            "ORtg",
            "DRtg",
            "NRtg",
            "ASTpG",
            "AST%",
            "AST/TOV",
            "DRBpG",
            "ORBpG",
            "TRBpG",
            "DRB%",
            "ORB%",
            "TRB%",
            "TOV%",
            "EFG%",
            "TSA",
            "TS%",
            "Pace",
            "TIE",
        ]

        self.__advanced_statistics_dataframe = pd.DataFrame(columns=self.__headings)

    def get_advanced_statistics_dataframe(self) -> pd.DataFrame:
        """
        Retrieve an advanced statistics populated with the team's advanced statistics for the given season.

        :return: The team's advanced statistics dataframe.
        :rtype: DataFrame
        """

        self.__populate_dataframe()

        return self.__advanced_statistics_dataframe

    def __get_dataframes(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Retrieve populated dataframes for both the team's statistics and their opponents' statistics.

        :return: Team's statistics dataframe and team's opponents' statistics dataframe.
        :rtype: tuple[DataFrame, DataFrame]
        """

        this_season_statistics = SeasonStatistics(self.__team_abbreviation, self.__year)

        return (
            this_season_statistics.get_team_dataframe(),
            this_season_statistics.get_opponent_dataframe(),
        )

    def __create_advanced_statistics(self) -> dict[str, float]:
        """
        Populate dictionary with calculated advanced statistics.

        :return: Dictionary of advanced statistics.
        :rtype: dict[str, float]
        """

        return {
            "PPG": self.__per_game(self.__points),
            "PAPG": self.__per_game(self.__opponent_points),
            "ORtg": self.__calculate_offensive_rating(),
            "DRtg": self.__calculate_defensive_rating(),
            "NRtg": self.__calculate_net_rating(),
            "ASTpG": self.__per_game(self.__assists),
            "AST%": self.__calculate_assist_rate(),
            "AST/TOV": self.__calculate_assist_to_turnover_ratio(),
            "DRBpG": self.__per_game(self.__defensive_rebounds),
            "ORBpG": self.__per_game(self.__offensive_rebounds),
            "TRBpG": self.__per_game(self.__total_rebounds),
            "DRB%": self.__calculate_defensive_rebound_percentage(),
            "ORB%": self.__calculate_offensive_rebound_percentage(),
            "TRB%": self.__calculate_total_rebound_percentage(),
            "TOV%": self.__calculate_turnover_percentage(),
            "EFG%": self.__calculate_effective_field_goal_percentage(),
            "TSA": self.__calculate_true_shooting_attempts(),
            "TS%": self.__calculate_true_shooting_percentage(),
            "Pace": self.__calculate_pace(),
            "TIE": self.__calculate_team_impact_estimate(),
        }

    def __per_game(self, statistic: float) -> float:
        """
        Retrieve a statistic's 'per game' value given its counting statistic value.

        :param statistic: The particular counting statistic.
        :type statistic: float
        :return: The statistic in 'per game' format, rounded to three decimal places.
        :rtype: float
        """

        return round(statistic / self.__games, 3)

    def __calculate_offensive_rating(self) -> float:
        """
        Calculate the team's offensive rating.

        Offensive rating is defined as the points scored by a team, per 100 possessions.

        :return: The team's offensive rating, rounded to three decimal places.
        :rtype: float
        """

        possessions = self.__calculate_possessions()

        return round((self.__points / possessions) * 100, 3)

    def __calculate_defensive_rating(self) -> float:
        """
        Calculate the team's defensive rating.

        Defensive rating is defined as the points allowed by a team, per 100 possessions.

        :return: The team's defensive rating, rounded to three decimal places.
        :rtype: float
        """

        opponent_possessions = self.__calculate_opponent_possessions()

        return round((self.__opponent_points / opponent_possessions) * 100, 3)

    def __calculate_net_rating(self) -> float:
        """
        Calculate the team's net rating.

        Net rating is defined as the difference between a team's offensive and defensive ratings.

        :return: The team's net rating, rounded to three decimal places.
        :rtype: float
        """

        offensive_rating = self.__calculate_offensive_rating()
        defensive_rating = self.__calculate_defensive_rating()

        return round(offensive_rating - defensive_rating, 3)

    def __calculate_assist_rate(self) -> float:
        """
        Calculate the team's assist rate.

        Assist rate is defined as the percentage of a team's field goals that are scored as a result of an assist from a
        team-mate.

        :return: The team's assist rate, rounded to three decimal places.
        :rtype: float
        """

        return round((self.__assists / self.__field_goals) * 100, 3)

    def __calculate_assist_to_turnover_ratio(self) -> float:
        """
        Calculate the team's assist/turnover ratio.

        Assist/turnover ratio is defined as the number of assists that a team records for every turnover they commit.

        :return: The team's assist/turnover ratio, rounded to three decimal places.
        :rtype: float
        """

        return round(self.__assists / self.__turnovers, 3)

    def __calculate_defensive_rebound_percentage(self) -> float:
        """
        Calculate the team's defensive rebounding rate.

        Defensive rebounding rate is defined as the percentage of defensive rebounds a team records from the total
        number of defensive rebounding opportunities.

        :return: The team's defensive rebounding rate, rounded to three decimal places.
        :rtype: float
        """

        return round(
            (
                self.__defensive_rebounds
                / (self.__defensive_rebounds + self.__opponent_offensive_rebounds)
            )
            * 100,
            3,
        )

    def __calculate_offensive_rebound_percentage(self) -> float:
        """
        Calculate the team's offensive rebounding rate.

        Offensive rebounding rate is defined as the percentage of offensive rebounds a team records from the total
        number of offensive rebounding opportunities.

        :return: The team's offensive rebounding rate, rounded to three decimal places.
        :rtype: float
        """

        return round(
            (
                self.__offensive_rebounds
                / (self.__offensive_rebounds + self.__opponent_defensive_rebounds)
            )
            * 100,
            3,
        )

    def __calculate_total_rebound_percentage(self) -> float:
        """
        Calculate the team's rebounding rate.

        Rebounding rate is defined as the percentage of rebounds a team records from the total number of rebounding
        opportunities.

        :return: The team's rebounding rate, rounded to three decimal places.
        :rtype: float
        """

        return round(
            (
                self.__total_rebounds
                / (self.__total_rebounds + self.__opponent_total_rebounds)
            )
            * 100,
            3,
        )

    def __calculate_turnover_percentage(self) -> float:
        """
        Calculate the team's turnover rate.

        Turnover rate is defined as an estimate for the percentage of plays a team carries out that result in a
        committed turnover.

        :return: The team's turnover rate, rounded to three decimal places.
        :rtype: float
        """

        return round(
            100
            * self.__turnovers
            / (
                self.__field_goal_attempts
                + (0.44 * self.__free_throw_attempts)
                + self.__turnovers
            ),
            3,
        )

    def __calculate_effective_field_goal_percentage(self) -> float:
        """
        Calculate the team's effective field goal percentage.

        Effective field goal percentage is defined as a metric that adjusts for the fact that a three-point field goal
        is worth more than a two-point field goal, giving a more accurate representation of a team's point scoring
        ability.

        :return: The team's effective field goal percentage, rounded to three decimal places.
        :rtype: float
        """

        return round(
            (
                (self.__field_goals + (0.5 * self.__three_point_makes))
                / self.__field_goal_attempts
            )
            * 100,
            3,
        )

    def __calculate_true_shooting_attempts(self) -> float:
        """
        Calculate the team's true shooting attempts.

        True shooting attempts is defined as the total number of attempts a team takes at scoring points, including 44%
        of free throw attempts.

        :return: The team's true shooting attempts, rounded to three decimal places.
        :rtype: float
        """

        return round(
            self.__field_goal_attempts + (0.44 * self.__free_throw_attempts), 3
        )

    def __calculate_true_shooting_percentage(self) -> float:
        """
        Calculate the team's true shooting percentage.

        True shooting percentage is defined as a measure of shooting efficiency that takes two-point and three-point
        field goals as well as free throws into account.

        :return: The team's true shooting percentage, rounded to three decimal places.
        :rtype: float
        """

        true_shooting_attempts = self.__calculate_true_shooting_attempts()

        return round((self.__points / (2 * true_shooting_attempts)) * 100, 3)

    def __calculate_possessions(self) -> float:
        """
        Calculate an estimate for the team's total possessions.

        The possessions metric is defined as an estimate for a team's total number of possessions given both theirs and
        their opponents' statistics.

        :return: The team's possessions, rounded to three decimal places.
        :rtype: float
        """

        return round(
            0.5
            * (
                (
                    self.__field_goal_attempts
                    + (0.4 * self.__free_throw_attempts)
                    - (
                        1.07
                        * (
                            self.__offensive_rebounds
                            / (
                                self.__offensive_rebounds
                                + self.__opponent_defensive_rebounds
                            )
                        )
                        * (self.__field_goal_attempts - self.__field_goals)
                    )
                    + self.__turnovers
                )
                + (
                    self.__opponent_field_goal_attempts
                    + (0.4 * self.__opponent_free_throw_attempts)
                    - (
                        1.07
                        * (
                            self.__opponent_offensive_rebounds
                            / (
                                self.__opponent_offensive_rebounds
                                + self.__defensive_rebounds
                            )
                        )
                        * (
                            self.__opponent_field_goal_attempts
                            - self.__opponent_field_goals
                        )
                    )
                    + self.__opponent_turnovers
                )
            ),
            3,
        )

    def __calculate_opponent_possessions(self) -> float:
        """
        Calculate an estimate for the team's opponents' total possessions.

        The possessions metric is defined as an estimate for a team's total number of possessions given both theirs and
        their opponents' statistics.

        :return: The team's opponents' possessions, rounded to three decimal places.
        :rtype: float
        """

        return round(
            0.5
            * (
                (
                    self.__opponent_field_goal_attempts
                    + (0.4 * self.__opponent_free_throw_attempts)
                    - (
                        1.07
                        * (
                            self.__opponent_offensive_rebounds
                            / (
                                self.__opponent_offensive_rebounds
                                + self.__defensive_rebounds
                            )
                        )
                        * (
                            self.__opponent_field_goal_attempts
                            - self.__opponent_field_goals
                        )
                    )
                    + self.__opponent_turnovers
                )
                + (
                    self.__field_goal_attempts
                    + (0.4 * self.__free_throw_attempts)
                    - (
                        1.07
                        * (
                            self.__offensive_rebounds
                            / (
                                self.__offensive_rebounds
                                + self.__opponent_defensive_rebounds
                            )
                        )
                        * (self.__field_goal_attempts - self.__field_goals)
                    )
                    + self.__turnovers
                )
            ),
            3,
        )

    def __calculate_pace(self) -> float:
        """
        Calculate an estimate for the team's pace.

        Pace factor is defined as an estimate for a team's total number of possessions per 48 minutes.

        :return: The team's pace, rounded to three decimal places.
        :rtype: float
        """

        possessions = self.__calculate_possessions()
        opponent_possessions = self.__calculate_opponent_possessions()

        return round(
            48 * ((possessions + opponent_possessions) / (2 * (self.__minutes / 5))), 3
        )

    def __calculate_team_impact_estimate(self) -> float:
        """
        Calculate the team's impact estimate.

        Team impact estimate is defined as an estimate for the percentage of total game actions that are enacted by a
        team.

        :return: The team's impact estimate, rounded to three decimal places.
        :rtype: float
        """

        return round(
            (
                (
                    self.__points
                    + self.__field_goals
                    + self.__free_throws
                    - self.__field_goal_attempts
                    - self.__free_throw_attempts
                    + self.__defensive_rebounds
                    + (self.__offensive_rebounds / 2)
                    + self.__assists
                    + self.__steals
                    + (self.__blocks / 2)
                    - self.__personal_fouls
                    - self.__turnovers
                )
                / (
                    (self.__points + self.__opponent_points)
                    + (self.__field_goals + self.__opponent_field_goals)
                    + (self.__free_throws + self.__opponent_free_throws)
                    - (self.__field_goal_attempts + self.__opponent_field_goal_attempts)
                    - (self.__free_throw_attempts + self.__opponent_free_throw_attempts)
                    + (self.__defensive_rebounds + self.__opponent_defensive_rebounds)
                    + (
                        (self.__offensive_rebounds + self.__opponent_offensive_rebounds)
                        / 2
                    )
                    + (self.__assists + self.__opponent_assists)
                    + (self.__steals + self.__opponent_steals)
                    + ((self.__blocks + self.__opponent_blocks) / 2)
                    - (self.__personal_fouls + self.__opponent_personal_fouls)
                    - (self.__turnovers + self.__opponent_turnovers)
                )
            )
            * 100,
            3,
        )

    def __populate_dataframe(self) -> None:
        """
        Populate the advanced statistics dataframe with the advanced statistics row.
        """

        self.__advanced_statistics_dataframe.loc[
            len(self.__advanced_statistics_dataframe)
        ] = self.__create_advanced_statistics()


if __name__ == "__main__":
    this_advanced_stats = TeamAdvancedStatistics("DEN", "2023")
    print(this_advanced_stats.create_advanced_statistics())
