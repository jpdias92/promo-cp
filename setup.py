from setuptools import setup

setup(
    name = 'promo',
    version = '0.1.0',
    packages = ['promo'],
    install_requires=[
        'bs4',
        'selenium',
    ],
    entry_points = {
        'console_scripts': [
            'promo = promo.__main__:main'
        ]
    })