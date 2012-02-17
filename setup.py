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
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Topic :: System :: Logging',
        ],
      packages=['logging_tree', 'logging_tree.tests'],
      )
