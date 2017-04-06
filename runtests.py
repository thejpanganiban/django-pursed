#!/usr/bin/env python
import os
import sys

import django

from django.conf import settings
from django.test.utils import get_runner


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()

    if sys.argv[0] == 'runtests.py' and len(sys.argv) == 2:
        suite = ['' + sys.argv[1]]
    else:
        suite = ['tests']

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(suite, verbosity=1, interactive=True)

    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
