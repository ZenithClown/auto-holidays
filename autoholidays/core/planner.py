# -*- encoding: utf-8 -*-

"""
A Core Auto-Holiday Planning
"""

import datetime as dt

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
