from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requires = [line.strip() for line in f.readlines()]

setup(
    name='ocam',
    version='0.1',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'convert_intrinsics_to_matlab_cli = ocam.matlab_wrapper:convert_intrinsics_to_matlab_cli',
            'convert_matlab_to_intrincis_cli = ocam.matlab_wrapper:convert_matlab_to_intrincis_cli',
        ],
    },
)
