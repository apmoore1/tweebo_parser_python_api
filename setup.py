from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='tweebo_parser_python_api',
      version='1.0.0',
      description='Python 3 API to the TweeboParser',
      url='https://github.com/apmoore1/tweebo_parser_python_api',
      author='Andrew Moore',
      author_email='andrew.p.moore94@gmail.com',
      license='GPLv3',
      install_requires=[
          'requests>=2.18.4'
      ],
      packages=['tweebo_parser'],
      zip_safe=False,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing'
        'Topic :: Text Processing :: Linguistic',
      ])
