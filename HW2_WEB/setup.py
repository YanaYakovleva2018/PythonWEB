from setuptools import setup, find_namespace_packages

setup(
    name='abvad',
    version='1.0.2',
    description='Very helpful assistant bot',
    url='https://github.com/VadimTrubay/abvad.git',
    author='Trubay_Vadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['numexpr'],
    entry_points={'console_scripts': ['abvad=abvad.main:main']},
    package_data={'abvad': ['abvad/*.txt', 'abvad/*.bin']}
)