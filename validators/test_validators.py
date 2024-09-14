from distutils.core import setup

import pytest
from typing import Any

from validators.validators import (
    OneOf,
    NumberValidator,
    StringValidator,
    PathValidator
)


# class TestValidator:
#     kind = OneOf('wood', 'metal', 'plastic')
#     num = NumberValidator(-100, 100)
#     desc = StringValidator(5, 10, str.isupper)
#     path = PathValidator('.py', os.path.isfile)
#
#     def __init__(
#             self,
#             kind: str,
#             num: int | float,
#             desc: str,
#             path: str | Path
#     ) -> None:
#         self.kind: str = kind
#         self.num: int | float = num
#         self.desc: str = desc
#         self.path: str | Path = path


# test = TestValidator(
#     kind='wood',
#     num=-55,
#     desc='ABCDEF',
#     path=Path('__init__.py')
# )

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
    pass



# test.kind = 'aluminum'
# test.kind = 5.5
#
# test.num = -1000
# test.num = '55'
#
# test.desc = 'ABC'
# test.desc = 'abcdef'
# test.desc = 101
#
# test.path = Path('test.py')
# test.path = r'test/test/test/test.csv'
# test.path = Path(__file__).parent
# test.path = Path(__file__).parent.parent / 'credentials.json'
