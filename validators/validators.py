import os
from pathlib import Path
from typing import Any, Optional, Callable, Iterable
from abc import ABC, abstractmethod


class Validator(ABC):
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
    def __init__(self, *options: Any) -> None:
        self.options: set[Any] = set(options)

    def validate(self, value: Any) -> None:
        if value not in self.options:
            raise ValueError(f'Expected {value!r} to be one of {self.options!r}')


class NumberValidator(Validator):
    def __init__(
        self,
        minvalue: Optional[int | float] = None,
        maxvalue: Optional[int | float] = None,
    ) -> None:
        self.minvalue: Optional[int | float] = minvalue
        self.maxvalue: Optional[int | float] = maxvalue

    def validate(self, value: Any) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(f'Expected {value!r} to be an int or float')

        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(f'Expected {value!r} to be at least {self.minvalue!r}')

        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(f'Expected {value!r} to be no more than {self.maxvalue!r}')


class StringValidator(Validator):
    def __init__(
        self,
        minsize: Optional[int] = None,
        maxsize: Optional[int] = None,
        predicate: Optional[Callable] = None,
    ) -> None:
        self.minsize: Optional[int] = minsize
        self.maxsize: Optional[int] = maxsize
        self.predicate: Optional[Callable[[Any], bool]] = predicate

    def validate(self, value: Any) -> None:
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
    def __init__(
        self,
        suffix: Optional[str | Iterable[str]] = None,
        predicate: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        self.suffix: Optional[str | Iterable[str]] = suffix
        self.predicate: Optional[Callable[[Any], bool]] = predicate

    def validate(self, value: Any) -> None:
        if not isinstance(value, (str, Path)):
            raise TypeError(f'Expected {value!r} to be a str or pathlib.Path type')

        if isinstance(value, Path):
            self.validate(str(value))

        if not os.path.exists(value):
            raise FileExistsError(f'Path {value!r} doesn\'t exist')

        if self.predicate is not None and not self.predicate(value):
            raise ValueError(f'Expected {self.predicate} to be true for {value!r}')

        if self.suffix is not None:
            if isinstance(self.suffix, str):
                self.suffix = [self.suffix]

            if os.path.splitext(value)[1] not in self.suffix:
                raise Exception(f'Expected {value!r} to be {self.suffix} file')
