import os
import pytest
from typing import Any
from pathlib import Path
from unittest.mock import MagicMock

from validators.validators import OneOf, NumberValidator, StringValidator, PathValidator


class TestOneOf:
    @pytest.mark.parametrize('value', [4, 'value4'])
    def test_oneof_raises_error_with_value_out_of_list(self, value: Any) -> None:
        validator = OneOf(1, 2, 3, 'value1', 'value2', 'value3')
        with pytest.raises(Exception):
            validator.validate(value)


class TestNumberValidator:
    @pytest.mark.parametrize('value', ['string', -200, 200])
    def test_numbervalidator_raises_error(self, value: Any) -> None:
        validator = NumberValidator(minvalue=-100, maxvalue=100)
        with pytest.raises(Exception):
            validator.validate(value)


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
