from setuptools import setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name='pyseus',
    version='0.1',
    description="",
    long_description=readme,
    long_description_content_type="text/markdown",
    url='http://github.com/calmer/pyseus',
    author='Christoph Almer',
    author_email='christoph.almer@gmail.com',
    license='GNU',
    packages=['pyseus'],
    install_requires=[
        '',
    ],
    zip_safe=False
)
