# -*- encoding: utf-8 -*-

"""
A Schema to Establish the Leaves of a User

A person typically have two types of leaves - weekly leave and other
leaves like sick leave, casual leave, etc. This schema is used to
establish the leaves of a user.
"""

from pydantic import BaseModel, field_validator
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
