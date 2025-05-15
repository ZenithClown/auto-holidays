# -*- encoding: utf-8 -*-

"""
A Utility Base Model to define a Person

A person is an end user who is going to consume the API to find the
best possible leave. The module provides the ability to find the best
possible combination for a single or a group of person, thus defining
a structured people's construct is essential.
"""

import datetime as dt

from pydantic import BaseModel

from autoholidays.utils.leaves import (
    LeaveCycle,
    CustomLeaves,
    CompWeeklyLeave
)
from autoholidays.utils.calender import MonthDayConstruct

class PersonConstruct(BaseModel):
    """
    Defination of a Enduser or a Person

    The person constuct is defined considering defualt attributes and
    properties which might be required to find the optimal holidays.

    :type  name: str
    :param name: A string representing the name of the person, this
        can be anything can beused to save the object.
    """

    name : str
    cycle : LeaveCycle = LeaveCycle(
        year = dt.date.today().year,
        _s = MonthDayConstruct(day = 1, month = 1),
        _e = MonthDayConstruct(day = 31, month = 12)
    )

    # now we can define the leaves for the person
    comp_week_off = CompWeeklyLeave()
    custom_leaves = list[CustomLeaves]
