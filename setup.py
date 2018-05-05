from setuptools import setup, find_packages

VERSION = '0.1'

setup(
    name='monypy',
    version=VERSION,
    description='Asynchronous lightweight ODM for mongodb',
    keywords='asyncio mongodb',
    url='http://github.com/nede1/monypy',

    author='Yaroslav Unknown',
    author_email='yaroslav@gmx.it',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'
    ],

    packages=find_packages(exclude=['tests*']),
    install_requires=['motor>=1.2.0'],
    setup_requires=['pytest-asyncio', 'flake8'],
    tests_require=['pytest-asyncio']
)
