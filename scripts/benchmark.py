import time
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

from mailcap_fix import mailcap_fix
from mailcap_fix import mailcap_original

MAILCAP_SHORT = os.path.join(ROOT, 'tests', 'data', 'mailcap_short.txt')
MAILCAP_LONG = os.path.join(ROOT, 'tests', 'data', 'mailcap_long.txt')


def timer(f, *args, **kwargs):
    n = 1000
    print('    %s loops, 3 repeats' % n)
    for _ in range(3):
        start = time.time()
        for _ in range(n):
            f(*args, **kwargs)
        elapsed_time = time.time() - start
        print('    %s ms per loop' % (elapsed_time / float(n) * 1000.0))


def lookup_all(lookup_func, d):
    # Loop through the mailcap dict and run a lookup for every MIME type
    for key in d:
        lookup_func(d, key)


if __name__ == '__main__':

    for filename in (MAILCAP_SHORT, MAILCAP_LONG):
        os.environ['MAILCAPS'] = filename

        print('MAICAPS=%s, mailcap_original.getcaps()' % filename)
        timer(mailcap_original.getcaps)

        print('MAICAPS=%s, mailcap_fix.getcaps()' % filename)
        timer(mailcap_fix.getcaps)

        d = mailcap_original.getcaps()
        print('MAICAPS=%s, mailcap_original.lookup(d, ...), %s entries' %
              (filename, len(d)))
        timer(lookup_all, mailcap_original.lookup, d)

        d_fix = mailcap_fix.getcaps()
        print('MAICAPS=%s, mailcap_fix.lookup(d_fix, ...), %s entries' %
              (filename, len(d_fix)))
        timer(lookup_all, mailcap_fix.lookup, d_fix)
