import os
from setuptools import setup

setup (name="pytraffic",
       version="0.1",
       packages=['pytraffic'],
       package_data={'pytraffic':  ['examples/*.py', 'examples/*.png']},
       include_package_data=True,
       install_requires=['pygame', 'docopt', 'numpy'])
