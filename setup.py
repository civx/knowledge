from setuptools import setup, find_packages

import multiprocessing
import logging

setup(
        name="knowledge",
        version="0.3",
        author="Luke Macken",
        author_email="lmacken@redhat.com",
        install_requires=['sqlalchemy'],
        tests_require=['nose'],
        test_suite='nose.collector',
        packages=find_packages(exclude=['ez_setup']),
        zip_safe=True,
      )
