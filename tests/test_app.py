import datetime
from unittest import TestCase
from unittest.mock import Mock, patch

import promo_cp


class TestDocumentDaoEs(TestCase):

    @patch.object(promo_cp, 'datetime', Mock(wraps=datetime))
    def test_get_applicable_dates_in_range(self):
        promo_cp.datetime.datetime.now.return_value = datetime.datetime(2018, 9, 26)

        self.assertEqual(1, len(promo_cp.get_applicable_dates_in_range(5, [4])),
                         "There is only 1 Friday in a 5 day range from 26/09/2018")

        self.assertEqual(13, len(promo_cp.get_applicable_dates_in_range(90, [4])),
                         "There are 13 Fridays in a 90 day range from 26/09/2018")




