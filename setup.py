try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'rannsaka - stochastic test harness for OpenStack projects',
    'author': 'pcrews',
    'url': 'https://github.com/pcrews/rannsaka',
    'download_url': 'https://github.com/pcrews/rannsaka.',
    'author_email': 'gleebix@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['rannsaka'],
    'scripts': [],
    'name': 'rannsaka'
}

setup(**config)

