from setuptools import setup


with open('README.md') as f:
    long_description = f.read()


setup(name='Chaturanga',
      version='0.1.2',
      description='Chess API for python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Cheran-Senthil/Chaturanga',
      author='Cheran',
      license='MIT',
      packages=['chaturanga'],
      install_requires=[
          'six',
          'termcolor',
      ])
