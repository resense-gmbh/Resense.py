from distutils.core import setup

setup(
    name='resensepy',
    version='0.0.2',
    packages=['resensepy'],
    package_dir={'resensepy': 'src/resense'},
    url='http://resense.io/',
    license='GPL-2.0',
    author='WittensteinSE',
    author_email='elias.hoerner@wittenstein.de',
    description='Python library for interfacing with the WITTENSTEIN HEX force/torque sensors',
    install_requires=[
        'numpy',
        'pyserial',
        'matplotlib'
    ],
)
