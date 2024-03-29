# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'pettoys',
    spider       = 'pet_toys',
    description  = 'Scrapy project for pettoys from madeinchina.com',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = pettoys.settings']},
    package_data= {'pettoys': ['*.json', '*.csv']},
)
