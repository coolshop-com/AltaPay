from setuptools import setup, find_packages


def get_version():
    return __import__('altapay').__version__


def get_url():
    return __import__('altapay').__github_url__

version = get_version()
github_url = get_url()

with open('README.rst', 'r') as f:
    readme = f.read()

with open('CHANGELOG.rst', 'r') as f:
    changelog = f.read()

requires = [
    'requests',
    'six'
]

setup(
    name='altapay',
    version=version,
    url=github_url,
    license='MIT',
    description='Unofficial Python SDK for AltaPay (formerly Pensio).',
    long_description=readme + '\n\n' + changelog,
    author='Coolshop.com',
    author_email='altapaysdk@coolshop.com',
    packages=find_packages(where='.', exclude=('tests*',)),
    install_requires=requires,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ])
