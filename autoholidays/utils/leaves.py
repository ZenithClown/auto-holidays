# -*- encoding: utf-8 -*-

"""
A Schema to Establish the Leaves of a User

A person typically have two types of leaves - weekly leave and other
leaves like sick leave, casual leave, etc. This schema is used to
establish the leaves of a user.
"""

from enum import Enum

from pydantic import (
    BaseModel,
    computed_field,
    field_validator
)

from autoholidays.errors import InvalidDayNum


class ENUMDays(Enum):
    """
    ENUM for the Days of the Week

    The days of the week is zero-indexed and starts from Monday. The
    values are in-sync with the :mod:`datetime` module in Python, thus
    providing backward compatibility.

    .. code-block:: python

        ENUMDays.SUNDAY # get the object for Sunday

        # to get/search for a particular day, use:
        print(ENUMDays(2))
        >> ENUMDays.WEDNESDAY

    The enum provides to distinct useful methods - :attr:`.name` to
    get the name defined in the enum and :attr:`.value` to get the
    value associated with the enum.

    Once the enum is extended to other pydantic base models, we can
    directly use the value without field validation as the value is
    already validated by the enum.
    """

    MONDAY    = 0
    TUESDAY   = 1
    WEDNESDAY = 2
    THURSDAY  = 3
    FRIDAY    = 4
    SATURDAY  = 5
    SUNDAY    = 6


    @classmethod
    def __override_error__(cls, value) -> None:
        """
        Raise an Custom Error if the Value is not in Range
        """

        raise InvalidDayNum(
            "`%r` is not a Valid `%s`. Valid Values: `%s`" % (
                value,
                cls.__name__,
                ", ".join([str(day.value) for day in cls])
            )
        )


class WeeklyLeave(BaseModel):
    """
    Weekly-Off Leave Schema/Construct Definition

    The weekly leave schema defines the days of the week when a user
    has a holiday. The days are typically Sunday and Saturday, and
    is same as the weekly off days for an organization.

    :type  days: set[ENUMDays]
    :param days: A set of :class:`ENUMDays` enum values representing
        the days of the week when a user has a holiday. The days are
        typically Sunday and Saturday, and is same as the weekly off.
        Defaults to Saturday and Sunday.

    Example Usage
    -------------

    The weeklc construct is significantly useful to find if a particular
    day is a weekly-off day or not. For example:

    .. code-block:: python

        import datetime as dt
        import autoholidays as ah

        # let's define a day to simulate the leave
        cur_date = dt.date(2025, 5, 4)

        # let's define the weekly leave construct with defaults
        weekly = ah.utils.WeeklyLeave()
        dayset = set([day.value for day in weekly.days])

        # check for each day if it is a weekly-off day or not
        print(f"Weekly Off: {cur_date.weekday() in dayset}")
        >> Weekly Off: True

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

    days : set[ENUMDays] = {
        ENUMDays.SUNDAY,
        ENUMDays.SATURDAY
    }


class CustomLeaveConstraint(BaseModel):
    """
    Allow to Put a Constraint on the Custom Leave Days
    
    The constraint is a advanced usage, that helps to put limitations
    on the custom leave days. For example, many organization do not
    allow to take a leave on a particular day of the week, or a
    particular day of the month. Another example of a constraint
    could be that an organization only not allow to take a particular
    leave n-times a year also maybe limiting the number of days.

    :type  limitweekdays: set[int]
    :param limitweekdays: A set of integers representing the days of
        the week where the user is not allowed to take a leave.
        Defaults to None.
    """

    limitweekdays : set[ENUMDays] = set()


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
