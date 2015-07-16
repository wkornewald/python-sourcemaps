from setuptools import setup, find_packages

DESCRIPTION = 'Python library for parsing and generating source maps'
LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

setup(name='python-sourcemaps',
      version='1.1',
      packages=find_packages(exclude=('tests', 'tests.*')),
      author='Waldemar Kornewald',
      author_email='wkornewald@gmail.com',
      url='https://bitbucket.org/allbuttonspressed/python-sourcemaps',
      license='BSD',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      platforms=['any'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'License :: OSI Approved :: BSD License',
      ],
)
