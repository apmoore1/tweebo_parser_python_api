from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='tweebo_parser_python_api',
      version='1.0.2',
      description='Python 3 API to the TweeboParser',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/apmoore1/tweebo_parser_python_api',
      author='Andrew Moore',
      author_email='andrew.p.moore94@gmail.com',
      license='GPLv3',
      install_requires=[
          'requests>=2.18.4'
      ],
      python_requires='>=3.6',
      packages=['tweebo_parser'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
      ])
