from setuptools import setup


with open('README.md') as f:
    long_description = f.read()


setup(name='Knights',
      version='0.0.1',
      description='Chess API for python',
      long_description=long_description,
      url='https://github.com/Cheran-Senthil/Knights',
      author='Cheran and Mukundan',
      license='MIT',
      packages=['knights'],
      install_requires=[
          'six',
          'termcolor',
      ])
