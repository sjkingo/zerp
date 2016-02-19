from setuptools import find_packages, setup

version = '0.2.0'

setup(
    name='zerp',
    version=version,
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
