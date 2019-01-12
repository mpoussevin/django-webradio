import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-webradio',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A simple web-based GUI for playing and managing online '
                'radio streams.',
    long_description=README,
    url='https://github.com/mpoussevin/django-webradio',
    author='Mickaël Poussevin',
    install_requires=[
        'python-vlc>=3.0.4106',
        'django>=2.1.5'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
