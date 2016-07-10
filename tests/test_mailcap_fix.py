import unittest
import mailcap
import random
import os

import mailcap_fix.mailcap as mailcap_fix


PATH = os.path.join(os.path.dirname(__file__), 'data')
TRIVIAL = os.path.join(PATH, 'trivial_mailcap')
EXTENDED = os.path.join(PATH, 'extended_mailcap')


class TestMailcapFix(unittest.TestCase):

    def test_sort_stable(self):
        """
        Sort should preserve list order if elements have equal values.
        Is this also true for pypy?

        Reference:
            https://docs.python.org/3/library/functions.html#sorted
        """

        entries = list(range(1000))
        random.shuffle(entries)
        self.assertEqual(entries, sorted(entries, key=lambda x: 1))

    def test_trivial(self):
        os.environ['MAILCAPS'] = TRIVIAL

        d = mailcap_fix.getcaps()
        self.assertEqual(d['image/*'][0]['lineno'], 0)

        command, entry = mailcap_fix.findmatch(d, 'image/png', filename='a')
        self.assertEqual(command, 'feh a')

        command, entry = mailcap_fix.findmatch(d, 'image/jpeg', filename='a')
        self.assertEqual(command, 'feh a')

        command, entry = mailcap_fix.findmatch(d, 'music/mp3', filename='a')
        self.assertEqual(command, 'play a')

    def test_backwards_compatible(self):
        os.environ['MAILCAPS'] = TRIVIAL

        d = mailcap.getcaps()
        d_lineno = mailcap_fix.getcaps()

        # Note: Both of these cases should not break, but they will exhibit the
        # old, incorrect behavior and return the second entry

        # Call the patched findmatch() using an  dict without ``lineno``
        command, entry = mailcap_fix.findmatch(d, 'image/jpeg', filename='a')
        self.assertEqual(command, 'eog a')

        # Call the original findmatch() using a dict with the added ``lineno``
        command, entry = mailcap.findmatch(d_lineno, 'image/jpeg', filename='a')
        self.assertEqual(command, 'eog a')

    def test_extended(self):
        os.environ['MAILCAPS'] = ':'.join([TRIVIAL, EXTENDED])

        # The line numbers should increment between files
        d = mailcap_fix.getcaps()
        self.assertEqual(d['image/*'][0]['lineno'], 0)
        self.assertEqual(d['text/plain'][0]['lineno'], 3)

        command, entry = mailcap_fix.findmatch(d, 'image/jpeg', filename='a')
        self.assertEqual(command, 'feh a')



if __name__ == '__main__':
    unittest.main()
