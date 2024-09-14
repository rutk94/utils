import os
import pytest
import math
import random
from pathlib import Path

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

class TestValidator:

    @pytest.fixture()
    def setup_5_random_int(self) -> list[int]:
        random.seed(1)
        return [random.randint(-100, 100) for _ in range(5)]

    @pytest.fixture()
    def setup_oneof_int(self, setup_5_random_int) -> OneOf:
        return OneOf(*setup_5_random_int)

    def test_oneof_raises_error(self, setup_oneof_int, setup_5_random_int) -> None:
        random.seed(None)
        value = random.randint(-100, 100)
        while value in setup_5_random_int:
            value = random.randint(-100, 100)

        with pytest.raises(ValueError):
            setup_oneof_int.validate(value)



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
