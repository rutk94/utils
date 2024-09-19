import os
import pytest
from typing import Any
from pathlib import Path

from validators.validators import OneOf, NumberValidator, StringValidator, PathValidator


class ClassWithDescriptor:
    value_one_of: OneOf = OneOf(1, 2, 3, 'value1', 'value2', 'value3')
    number: NumberValidator = NumberValidator(minvalue=-100, maxvalue=100)
    string: StringValidator = StringValidator(
        minsize=2, maxsize=5, predicate=str.islower
    )
    path: PathValidator = PathValidator('.py', predicate=os.path.isfile)

    def __init__(
        self,
        value_one_of: Any = 'value1',
        number: int | float = 0,
        string: str = 'abc',
        path: str | Path = Path(__file__),
    ) -> None:
        self.value_one_of: Any = value_one_of
        self.number: int | float = number
        self.string: str = string
        self.path: str | Path = path


class TestOneOf:
    @pytest.fixture(scope='class')
    def setup_class(self) -> ClassWithDescriptor:
        return ClassWithDescriptor(value_one_of='value1')

    def test_oneof_get_returns_right_value(self, setup_class: Any) -> None:
        assert setup_class.value_one_of == 'value1'

    def test_oneof_set_raises_error_with_wrong_value(self, setup_class: Any) -> None:
        with pytest.raises(Exception):
            setup_class.value_one_of = 'value4'
            _ = ClassWithDescriptor('value4')


class TestNumberValidator:
    @pytest.fixture(scope='class')
    def setup_class(self) -> ClassWithDescriptor:
        return ClassWithDescriptor(number=50)

    def test_numbervalidator_get_returns_right_value(self, setup_class: Any) -> None:
        assert setup_class.number == 50

    @pytest.mark.parametrize('wrong_value', ['string', -200, 200])
    def test_numbervalidator_set_raises_error_with_wrong_value(
        self, setup_class: Any, wrong_value: Any
    ) -> None:
        with pytest.raises(Exception):
            # check on existing object
            setup_class.number = wrong_value
            # check on creating new object
            _ = ClassWithDescriptor(number=wrong_value)


class TestStringValidator:
    @pytest.fixture(scope='class')
    def setup_class(self) -> ClassWithDescriptor:
        return ClassWithDescriptor(string='def')

    def test_stringvalidator_get_returns_right_value(self, setup_class: Any) -> None:
        assert setup_class.string == 'def'

    @pytest.mark.parametrize('wrong_value', [1, 5.5, 'a', 'ABC', 'abcdefghi'])
    def test_stringvalidator_set_raises_error_with_wrong_value(
        self, setup_class: Any, wrong_value: Any
    ) -> None:
        with pytest.raises(Exception):
            # check on existing object
            setup_class.string = wrong_value
            # check on creating new object
            _ = ClassWithDescriptor(string=wrong_value)


class TestPathValidator:
    @pytest.fixture(scope='class')
    def setup_class(self) -> ClassWithDescriptor:
        return ClassWithDescriptor(path=Path(__file__))

    def test_pathvalidator_get_returns_right_value(self, setup_class: Any) -> None:
        assert setup_class.path == Path(__file__)

    @pytest.mark.parametrize(
        'wrong_value', [123, r'test/test', Path('test.abc'), r'file/not/exists.py']
    )
    def test_pathvalidator_set_raises_error_with_bad_value(
        self, setup_class: Any, wrong_value: Any
    ) -> None:
        with pytest.raises(Exception):
            # check on existing object
            setup_class.path = wrong_value
            # check on creating new object
            _ = ClassWithDescriptor(path=wrong_value)
