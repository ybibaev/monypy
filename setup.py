import re

from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()

with open('monypy/__init__.py') as f:
    version = (
        re.search(
            r"__version__ = '([^']+)",
            f.read()
        ).group(1)
    )

setup(
    name='monypy',
    version=version,
    description='Asynchronous lightweight ODM for mongodb',
    keywords='asyncio mongodb',
    url='http://github.com/nede1/monypy',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Yaroslav Unknown',
    author_email='yaroslav@gmx.it',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: AsyncIO',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'
    ],

    packages=find_packages(exclude=['tests*']),
    install_requires=['motor>=1.2'],
    setup_requires=['pytest-asyncio', 'flake8'],
    tests_require=['pytest-asyncio']
)
