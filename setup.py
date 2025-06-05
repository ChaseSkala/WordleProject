from setuptools import setup, find_packages

setup(
    name='wordle_solver',
    version='0.94',
    packages=find_packages(),
    package_data={
        'wordle_solver': ['words.txt', 'startingwords.txt'],
    },
    install_requires=[],

    entry_points={
        'console_scripts': [
            'wordle_solver = wordle_solver.main:main'
        ]
    }
)