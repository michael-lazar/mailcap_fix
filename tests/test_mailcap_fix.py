import unittest

from mailcap_fix import mailcap


class TestMailcapFix(unittest.TestCase):

    def test_trivial(self):
        mailcap.getcaps()


if __name__ == '__main__':
    unittest.main()
