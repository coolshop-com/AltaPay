from setuptools import setup, find_packages


def get_version():
    return __import__('altapay').VERSION


version = get_version()

with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name='altapay',
    version=version,
    url='https://github.com/coolshop-com/AltaPay',
    license='MIT',
    description='Unofficial Python SDK for AltaPay (formerly Pensio).',
    long_description=long_description,
    author='Coolshop.com',
    author_email='altapaysdk@coolshop.com',
    packages=find_packages(where='.', exclude=('tests*',)),
    install_requires=[],
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
