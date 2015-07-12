try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A script to plot ELD grades.',
    'author': 'Greg Aitkenhead',
    'url': 'https://github.com/HarryLoofah/grade-data',
    'download_url': 'https://github.com/HarryLoofah/grade-data.git',
    'author_email': 'none',
    'version': '1.0',
    'install_requires': ['pandas,' 'matplotlib', 'datetime'],
    'license': ['MIT'],
    'packages': ['grade_data'],
    'scripts': [],
    'name': 'GradeData'
}

setup(**config)
