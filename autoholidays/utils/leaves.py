# -*- encoding: utf-8 -*-

"""
A Schema to Establish the Leaves of a User

A person typically have two types of leaves - weekly leave and other
leaves like sick leave, casual leave, etc. This schema is used to
establish the leaves of a user.
"""

from pydantic import (
    BaseModel,
    computed_field,
    field_validator
)

from autoholidays.errors import InvalidLeaveDays

class WeeklyLeave(BaseModel):
    """
    Weekly Leave Schema Definition

    The weekly leave schema defines the days of the week when a user
    has a holiday. The days are typically Sunday and Saturday, and
    is same as the weekly off days for an organization.

    :type  days: list[int]
    :param days: A list of integers representing the days of the week
        when the user has a holiday. The integers should be
        in the range of 0-6, where 0 is Sunday and 6 is Saturday. The
        zerobased indexed is preserved to provide backward compatibility
        with the :mod:`calendar` module in Python. The default value
        is [0, 6], which means Sunday and Saturday.

    Example Usage
    -------------

    The weeklc construct is significantly useful to find if a particular
    day is a weekly-off day or not. For example:

    .. code-block:: python

        import datetime as dt
        import autoholidays as ah

        # let's define a day to simulate the leave
        sunday = dt.date(2025, 5, 4)
        monday = dt.date(22025, 5, 5)

        # let's define the weekly leave construct with defaults
        weekly = ah.utils.WeeklyLeave()

        # check for each day if it is a weekly-off day or not
        # print(f"DATE: {sunday} (= Day of Week : {sunday.weekday()})")
        print(f"  >> Weekly Off: {sunday.weekday() in weekly.days}")
        >> Weekly Off: True

        # print(f"DATE: {monday} (= Day of Week : {monday.weekday()})")
        print(f"  >> Weekly Off: {monday.weekday() in weekly.days}")
        >> Weekly Off: False

    Leave Days Calculation
    ----------------------

    The leave days considers the days of a week and calculates the
    required number of leaves to be availaed. The weekly construct now
    can be used to calculate the number of leaves excluding the weekly
    off days.

    .. code-block:: text

        S M T W T F S
        0 1 2 3 4 5 6
        0 1 1 1 1 1 0 # number of leaves required

    Considering the default weekly-off days, the number of leaves to
    be availed is 5 (Monday to Friday), excluding the weekly-off days.
    """

    days : set[int] = {0, 6} # Sunday and Saturday


    @field_validator("days")
    @classmethod
    def validate_days(cls, value : set[int]) -> set[int]:
        """
        Validate the days of the week for weekly leave.

        The days should be in the range of 0-6, where 0 is Sunday and
        6 is Saturday. The zerobased indexed is preserved to provide
        backward compatibility with the :mod:`calendar` module in Python.

        :param value: A list of integers representing the days of the week
            when the user has a holiday.

        :return: A list of integers representing the days of the week
            when the user has a holiday.
        """

        min_, max_ = min(value), max(value)
        
        if min_ < 0 or max_ > 6:
            raise InvalidLeaveDays(f"Invalid leave days: {value}.")

        return value


class CustomLeaves(BaseModel):
    """
    A Custom Leaves Schema Definition

    A custom leave is any type of a named leave that a user can take,
    based on the organization policy. The custom leaves base model
    also allow to put any type of leave constraint on the leave days.

    :type  name: str
    :param name: A string representing the name of the custom leave.
        The name should be a valid string and should not be empty.
    """

    name : str

    @computed_field
    @property
    def shortname(self) -> str:
        """
        A Short Name for the Custom Leave
        
        The short name is an abbreviation of the custom leave name.
        The short name is auto calculated from the custom leave name
        by getting the first letter of each word in the name.
        """

        return "".join([word[0] for word in self.name.split()]).upper()
