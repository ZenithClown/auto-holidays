# -*- encoding: utf-8 -*-

"""
A Core Auto-Holiday Planning
"""

import datetime as dt
import datetime_ as dt_

from autoholidays.utils.calender import AnyCycle
from autoholidays.utils.person import PersonConstruct

class LeavePlanner:
    def __init__(
        self,
        period : AnyCycle,
        persons : list[PersonConstruct]
    ) -> None:
        self.start, self.end = period.start, period.end
        
        # a list of persons, this should be defined and passed
        # holiday construct are person wise, add them while defining
        self.persons = persons


    @property
    def calender(self) -> list:
        """
        Return the Calender of Dates from Start to End of Planning

        The property uses :mod:`datetime_` to get all the dates from
        start to end of planning days. The iterable list can then be
        extended to various other properties or methods to find and
        derive optimal result for the year.
        """

        return list(dt_.date_range(start = self.start, end = self.end))


    @property
    def plan_duration(self) -> int:
        """
        Return the Total No. of Days between Start and End
        """

        return (self.end - self.start).days


    @property
    def paid_holidays(self) -> dict[list]:
        """
        Returns a List of Paid Holidays per Person

        Each person has a set of weekly holidays and additional state
        holidays. The property returns an iterable of holidays for
        each defined person by returning an unique set of days sorted
        in ascending order. The key of the dictionary is same as the
        person :attr:`Person.name` attribute.
        """

        holidays = {
            person.name : dict(
                comp_week_off = [
                    date for date in self.calender
                    if date.weekday() in person.comp_week_off.day_values
                ],
                additional_holidays = [
                    holiday.date for holiday in person.additional_holidays
                ]
            )
            for person in self.persons
        }

        return {
            k : v | dict(
                unique = sorted(list(set(
                    v["comp_week_off"] + v["additional_holidays"]
                ))),
                nunique = len(sorted(list(set(
                    v["comp_week_off"] + v["additional_holidays"]
                ))))
            )
            for k, v in holidays.items()
        }


    @property
    def verbose_paid_holidays(self) -> dict:
        """
        Return a Verbose of Total Paid Holiday for Each Person
        """

        return {
            person.name : dict(
                total = self.paid_holidays[person.name]["nunique"],
                ratio = round(
                    self.paid_holidays[person.name]["nunique"] / self.plan_duration,
                    5
                )
            )
            for person in self.persons
        }
