import os
import random
from numbers import Number

import pytest
import numpy as np
from typing import Any
from pathlib import Path
from unittest.mock import MagicMock

from validators.validators import OneOf, NumberValidator, StringValidator, PathValidator

#TODO: test descriptor functionality

@pytest.mark.parametrize('right_values', [[1, 2, 3, 'value1', 'value2', 'value3']])
class TestOneOf:
    @pytest.fixture()
    def setup_validator(self, right_values: list[Any]) -> OneOf:
        return OneOf(*right_values)

    @pytest.fixture()
    def setup_right_value(self, right_values: list[Any]) -> Any:
        return right_values[0]

    @pytest.fixture()
    def setup_class(self, setup_validator: OneOf, setup_right_value: Any) -> Any:
        class ClassWithDescriptor:
            value: OneOf = setup_validator
            def __init__(self, value: Any) -> None:
                self.value: Any = value
        return ClassWithDescriptor(value=setup_right_value)

    @pytest.mark.parametrize('wrong_value', [4, 'value4'])
    def test_oneof_validate_raises_error_with_wrong_value(
            self, setup_validator: OneOf, wrong_value: Any
    ) -> None:
        with pytest.raises(Exception):
            setup_validator.validate(wrong_value)

    @pytest.mark.parametrize('wrong_value', [4, 'value4'])
    def test_oneof_set_raises_error_with_wrong_value(
            self, setup_class: Any, wrong_value: Any
    ) -> None:
        with pytest.raises(Exception):
            setup_class.value = wrong_value

    def test_oneof_get_returns_right_value(
            self, setup_class: Any, setup_right_value: Any
    ) -> None:
        assert setup_class.value == setup_right_value


@pytest.mark.parametrize('min_value, max_value', [(-100, 100)])
class TestNumberValidator:
    @pytest.fixture()
    def setup_validator(self, min_value: int | float, max_value: int | float) -> NumberValidator:
        return NumberValidator(minvalue=min_value, maxvalue=max_value)

    @pytest.fixture(params=[0.5, 1])
    def setup_right_value(
            self,  min_value: int | float, max_value: int | float, request: Any
    ) -> int | float:
        random.seed(100)
        step = request.param
        random_right_value: int | float = (
            random.choice(np.arange(min_value, max_value, step).tolist())
        )
        return random_right_value

    @pytest.fixture()
    def setup_class(self, setup_validator: NumberValidator, setup_right_value: int | float) -> Any:
        class ClassWithDescriptor:
            value: NumberValidator = setup_validator
            def __init__(self, value: int | float) -> None:
                self.value: int | float = value
        return ClassWithDescriptor(value=setup_right_value)

    @pytest.mark.parametrize('wrong_value', ['string', -200, 200])
    def test_numbervalidator_validate_raises_error_with_wrong_value(
            self, setup_validator: NumberValidator, wrong_value: Any
    ) -> None:
        with pytest.raises(Exception):
            setup_validator.validate(wrong_value)

    @pytest.mark.parametrize('wrong_value', ['string', -200, 200])
    def test_numbervalidator_set_raises_error_with_wrong_value(
            self, setup_class: Any, wrong_value: Any
    ) -> None:
        with pytest.raises(Exception):
            setup_class.value = wrong_value

    def test_numbervalidator_get_returns_right_value(
            self, setup_class: Any, setup_right_value: Any
    ) -> None:
        assert setup_class.value == setup_right_value


class TestStringValidator:
    @pytest.mark.parametrize('value', [123, 'abcdefghi', 'a', 'ABCDEF'])
    def test_stringvalidator_raises_error(self, value: Any) -> None:
        validator = StringValidator(minsize=2, maxsize=6, predicate=str.islower)
        with pytest.raises(Exception):
            validator.validate(value)


class TestPathValidator:
    @pytest.fixture()
    def setup_pathvalidator(self) -> PathValidator:
        return PathValidator(['.txt', '.csv', '.py'], os.path.isfile)

    def test_pathvalidator_raises_error_when_path_not_exist(
        self, setup_pathvalidator: PathValidator, monkeypatch: Any
    ) -> None:
        mock_not_exist = MagicMock(return_value=False)
        monkeypatch.setattr('os.path.exists', mock_not_exist)
        with pytest.raises(Exception):
            setup_pathvalidator.validate('test/test.py')

    @pytest.mark.parametrize('value', [123, r'test/test', Path('test.json')])
    def test_pathvalidator_raises_error_with_bad_value(
        self, setup_pathvalidator: PathValidator, value: Any, monkeypatch: Any
    ) -> None:
        mock_exist = MagicMock(return_value=True)
        monkeypatch.setattr('os.path.exists', mock_exist)
        with pytest.raises(Exception):
            setup_pathvalidator.validate(value)
