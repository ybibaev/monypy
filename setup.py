from setuptools import setup

setup(name='monypy',
      version='0.1a',
      description='async lightweight ODM for mongodb',
      url='http://github.com/nede1/monypy',
      author='Yaroslav Unknown',
      author_email='yaroslav@gmx.it',
      license='MIT',
      packages=['monypy'],
      install_requires=['motor'],
      zip_safe=False)
