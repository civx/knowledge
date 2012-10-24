from setuptools import setup, find_packages

setup(
        name="knowledge",
        version="0.2",
        author="Luke Macken",
        author_email="lmacken@redhat.com",
        install_requires=['sqlalchemy'],
        packages=find_packages(exclude=['ez_setup']),
        zip_safe=True,
      )
