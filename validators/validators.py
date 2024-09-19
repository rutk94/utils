import os
from pathlib import Path
from typing import Any, Optional, Callable
from abc import ABC, abstractmethod


class Validator(ABC):
    """Abstract class for validators with descriptor functionality"""

    def __set_name__(self, owner: Any, name: str) -> None:
        self.private_name = '_' + name

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        return getattr(obj, self.private_name)

    def __set__(self, obj: Any, value: Any) -> None:
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass


class OneOf(Validator):
    """
    Descriptor representing the list of acceptable values.

    Args:
        *options (Any): acceptable values

    Methods:
        validate(value: Any) -> None:
            Validates if /value/ fits in acceptable values /*options/.
            If not, raises ValueError.
    """

    def __init__(self, *options: Any) -> None:
        self.options: set[Any] = set(options)

    def validate(self, value: Any) -> None:
        """
        Validates whether /value/ fits in acceptable values /*options/.
        If not, raises ValueError.

        Args:
            value (Any): value to validate

        Returns:
            True -> None
            False -> raises ValueError
        """
        if value not in self.options:
            raise ValueError(f'Expected {value!r} to be one of {self.options!r}')


class NumberValidator(Validator):
    """
    Descriptor representing the acceptable range of numbers for a value.

    Args:
        minvalue (Optional[int | float]): minimal value in range
        maxvalue (Optional[int | float]): maximal value in range

    Methods:
        validate(value: Any) -> None:
            Validates whether /value/ is integer or float
            Validates whether /value/ fits in acceptable range of numbers
    """

    def __init__(
        self,
        minvalue: Optional[int | float] = None,
        maxvalue: Optional[int | float] = None,
    ) -> None:
        self.minvalue: Optional[int | float] = minvalue
        self.maxvalue: Optional[int | float] = maxvalue

    def validate(self, value: Any) -> None:
        """
        Validates whether /value/ is integer or float type
        Validates whether /value/ fits in acceptable range of numbers

        Args:
            value (Any): value to validate

        Returns:
            if True -> None
            if /value/ isn't integer of float -> raises TypeError
            if /value/ doesn't fit in range -> raises ValueError
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f'Expected {value!r} to be an int or float')

        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(f'Expected {value!r} to be at least {self.minvalue!r}')

        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(f'Expected {value!r} to be no more than {self.maxvalue!r}')


class StringValidator(Validator):
    """
    Descriptor representing parameters of acceptable string value

    Args:
        minsize (Optional[int]): minimal length of string value
        maxsize (Optional[int]): maximal length of string value
        predicate (Optional[Callable]):
            function which returns True/False being executed with string value
            e.g.
                str.isupper
            or
                lambda x: 'pattern' in x

    Methods:
        validate(value: Any) -> None:
            Validates whether /value/ is string type.
            Validates whether /value/ fits in length range
            Validates whether /value/ meets the /predicate/ condition
    """

    def __init__(
        self,
        minsize: Optional[int] = None,
        maxsize: Optional[int] = None,
        predicate: Optional[Callable] = None,
    ) -> None:
        self.minsize: Optional[int] = minsize
        self.maxsize: Optional[int] = maxsize
        self.predicate: Optional[Callable] = predicate

    def validate(self, value: Any) -> None:
        """
        Validates whether /value/ is string type.
        Validates whether /value/ fits in length range
        Validates whether /value/ meets the /predicate/ condition

        Args:
            value (Any): value to validate

        Returns:
            if True -> None
            if /value/ isn't string -> raises TypeError
            if /value/ doesn't fit in length range
                or doesn't meet the /predicate condition -> raises ValueError
        """
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be a str')

        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(
                f'Expected {value!r} to be no smaller than {self.minsize!r}'
            )

        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f'Expected {value!r} to be no bigger than {self.maxsize!r}'
            )

        if self.predicate is not None and not self.predicate(value):
            raise ValueError(f'Expected {self.predicate} to be true for {value!r}')


class PathValidator(Validator):
    """
    Descriptor representing parameters of acceptable path

    Args:
        *suffixes (Optional[str]): set of strings representing acceptable file suffixes
        predicate (Optional[Callable]):
            function which returns True/False being executed with string value
            e.g.
                str.isupper
            or
                lambda x: 'pattern' in x

    Methods:
        validate(value: Any) -> None:
            Validates whether /value/ is string or pathlib.Path type.
            Validates whether /value/ path exists.
            Validates whether /value/ meets /predicate/ condition
            Validates whether /value/ fits in acceplable suffixes set
    """

    def __init__(
        self,
        *suffixes: Optional[str],
        predicate: Optional[Callable] = None,
    ) -> None:
        self.predicate: Optional[Callable] = predicate
        self.suffixes: set[Optional[str]] = set(suffixes)

    def validate(self, value: Any) -> None:
        """
        Validates whether /value/ is string or pathlib.Path type.
        Validates whether /value/ path exists.
        Validates whether /value/ meets /predicate/ condition
        Validates whether /value/ fits in acceplable suffixes list

        Args:
            value (Any): value to validate

        Returns:
            if True -> None
            if /value/ isn't string or pathlib.Path type -> raises TypeError
            if /value/ path doesn't exist -> raises FileExistsError
            if /value/ doesn't meet /predicate/ condition
                or doesn't fit in acceplable suffixex list -> raises ValueError
        """
        if not isinstance(value, (str, Path)):
            raise TypeError(f'Expected {value!r} to be a str or pathlib.Path type')

        if isinstance(value, Path):
            self.validate(str(value))

        if not os.path.exists(value):
            raise FileExistsError(f'Path {value!r} doesn\'t exist')

        if self.predicate is not None and not self.predicate(value):
            raise ValueError(f'Expected {self.predicate} to be true for {value!r}')

        if self.suffixes is not None:
            if os.path.splitext(value)[1] not in self.suffixes:
                raise ValueError(f'Expected {value!r} to be {self.suffixes} file')
