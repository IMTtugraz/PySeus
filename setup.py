from io import open
from setuptools import setup, find_packages

setup(
    name = 'pyseus',
    version = '0.1',
    description = "PySeus is a minimal viewer for medical imaging data.",
    long_description = open('README.md', encoding='utf-8').read(),
    long_description_content_type = "text/markdown",
    url = 'http://github.com/calmer/pyseus',
    author = 'Christoph Almer',
    author_email = 'christoph.almer@gmail.com',
    license = 'GNU',
    packages = find_packages(),
    # package_data = {'pyseus': [
    # ]},
    # include_package_data = True,
    install_requires = [
        'PySide2',
        'numpy',
        'h5py',
    ],
    entry_points = {
        'console_scripts': [
            'pyseus = pyseus:_console_entry',
        ],
    },
    zip_safe = False
)
