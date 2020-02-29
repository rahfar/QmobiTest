import unittest
import value_converter


class Test(unittest.TestCase):
    def test_incorrect_input(self):
        self.assertRaises((Exception,), value_converter.convert_usd_to_rub, 'abc')

    def test_correct_input(self):
        try:
            value_converter.convert_usd_to_rub(100)
        except:
            self.fail(msg='converter failed')


if __name__ == '__main__':
    unittest.main()
