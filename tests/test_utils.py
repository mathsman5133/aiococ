import datetime
import unittest

from coc.players import Player
from coc.utils import correct_tag, from_timestamp, custom_isinstance


class DummyPlayerClass(Player):
    def __init__(self):
        super().__init__(data={"name": "", "tag": ""})


class UtilTests(unittest.TestCase):
    def test_correct_tag_remove_whitespace(self):
        self.assertEqual(correct_tag("   #G88CYQP  "), "#G88CYQP")
        self.assertEqual(correct_tag("  #  G88 CYQ P  "), "#G88CYQP")

    def test_correct_tag_add_prefix(self):
        self.assertEqual(correct_tag("G88CYQP"), "#G88CYQP")
        self.assertEqual(correct_tag("%G88CYQP"), "#G88CYQP")
        self.assertEqual(correct_tag("(*&!#$G88CYQP", prefix=":"), ":G88CYQP")

    def test_correct_tag_upper(self):
        self.assertEqual(correct_tag("#g88cyqp"), "#G88CYQP")
        self.assertEqual(correct_tag("#G88cyQP"), "#G88CYQP")

    def test_from_timestamp(self):
        test_cases = (
            ("20200115T045659.000Z", datetime.datetime(year=2020, month=1, day=15, hour=4, minute=56, second=59)),
            ("20200113T035456.000Z", datetime.datetime(year=2020, month=1, day=13, hour=3, minute=54, second=56)),
            ("20191214T033206.000Z", datetime.datetime(year=2019, month=12, day=14, hour=3, minute=32, second=6)),
            ("20191121T015147.000Z", datetime.datetime(year=2019, month=11, day=21, hour=1, minute=51, second=47)),
            ("20191027T235026.000Z", datetime.datetime(year=2019, month=10, day=27, hour=23, minute=50, second=26)),
            ("20180924T010738.000Z", datetime.datetime(year=2018, month=9, day=24, hour=1, minute=7, second=38)),
        )
        for raw_timestamp, expected in test_cases:
            self.assertEqual(from_timestamp(raw_timestamp), expected)

    def test_custom_isinstance(self):
        self.assertEqual(custom_isinstance(DummyPlayerClass(), __name__, "DummyPlayerClass"), True)
        self.assertEqual(
            custom_isinstance(DummyPlayerClass(), DummyPlayerClass.__module__, DummyPlayerClass.__name__), True
        )
        self.assertEqual(custom_isinstance(Player({"name": "", "tag": ""}), Player.__module__, Player.__name__), True)

        self.assertNotEqual(custom_isinstance(DummyPlayerClass(), __name__, "Clearly Not A Player"), True)
        self.assertNotEqual(custom_isinstance(DummyPlayerClass, __name__, "DummyPlayerClass"), True)
        self.assertNotEqual(custom_isinstance(Player({"name": "", "tag": ""}), __name__, "Player"), True)
