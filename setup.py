try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'den',
    'author': 'Quincey ten Kroode',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'qjv.tenkroode@gmail.com',
    'version': '0.1',
    'install_requires': [
        'nose',
        'coverage',
        'requests'],
    'packages': ['den'],
    'scripts': [],
    'name': 'den'
}

setup(**config)
