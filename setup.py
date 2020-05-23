from setuptools import setup, find_packages
#!/usr/bin/env python

setup(
    name='main',
    version='1.0.0',
    url='https://github.com/sarahnator/python-checkin.git',
    description='Program to facilitate analysis of myfitnesspal data in google spreadsheets',
    author='Sarah Etter',
    author_email='sarahett@usc.edu',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        checkin=main.scripts.checkin:cli
    ''',
)
