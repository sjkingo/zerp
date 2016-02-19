from setuptools import find_packages, setup

from zerp import __version__

setup(
    name='zerp',
    version=__version__,
    license='BSD',
    author='Sam Kingston',
    author_email='sam@sjkwi.com.au',
    description='zerp is a compiler for Z, a toy programming language similar in syntax to Python and Pascal. It targets a virtual machine written in Python that supports a limited instruction set.',
    url='https://github.com/sjkingo-archive/zerp',
    install_requires=[
        'multipledispatch',
        'ply',
    ],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Compilers',
        'Topic :: System :: Emulators',
    ],
)
