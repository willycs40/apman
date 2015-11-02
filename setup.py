from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os
import sys

import apman

here = os.path.abspath(os.path.dirname(__file__))

class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='apman',
    version=apman.__version__,
    url='https://github.com/willycs40/apman/',
    license='Apache Software License',
    author='Will Cubitt-Smith',
    tests_require=['pytest'],
    install_requires=[
                    'SQLAlchemy>=1.0.0',
                    ],
    cmdclass={'test': PyTest},
    author_email='will@apressci.co.uk',
    description='Python wrapper for running (analytic) applications in a controlled manner.',
    packages=['apman'],
    include_package_data=True,
    platforms='any',
    test_suite='tests.test_apman',
    scripts=['scripts/apman_run', 'scripts/apman_init'],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Server Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
        ],
    extras_require={
        'testing': ['pytest'],
    }
)