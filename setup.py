import re

from setuptools import find_packages, setup


def get_version():
    with open('altapay/__init__.py') as f:
        return re.search(
            r'^__version__\s*=\s*[\'"]([^\']*)[\'"]', f.read(),
            re.MULTILINE).group(1)


def get_url():
    with open('altapay/__init__.py') as f:
        return re.search(
            r'^__github_url__\s*=\s*[\'"]([^\']*)[\'"]', f.read(),
            re.MULTILINE).group(1)

version = get_version()
github_url = get_url()

with open('README.rst', 'r') as f:
    readme = f.read()

with open('CHANGELOG.rst', 'r') as f:
    changelog = f.read()

requires = [
    'responses',
    'requests',
    'six'
]

setup(
    name='altapay',
    version=version,
    url=github_url,
    license='MIT',
    description='Unofficial Python SDK for AltaPay (formerly Valitor/Pensio).',
    long_description=readme + '\n\n' + changelog,
    author='Coolshop.com',
    author_email='altapaysdk@coolshop.com',
    packages=find_packages(where='.', exclude=('tests*',)),
    install_requires=requires,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ])
