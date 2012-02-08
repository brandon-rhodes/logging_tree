from distutils.core import setup
import logging_tree

setup(name='logging_tree',
      version=logging_tree.__version__,
      description='Introspect and display the logger tree inside "logging"',
      long_description=logging_tree.__doc__,
      author='Brandon Rhodes',
      author_email='brandon@rhodesmill.org',
      url='https://github.com/brandon-rhodes/logging_tree',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Logging',
        ],
      packages=['logging_tree', 'logging_tree.tests'],
      )
