from setuptools import setup, find_packages
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.md')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='pi_walk_slope',
    version='0.0.0',
    description=('Performance Indicator computation for the Walking on slope protocol.'),
    long_description=long_description,
    author='RRD',
    author_email='whoever@rrd.com',
    url='https://github.com/',
    license='Beerware',
    packages= find_packages(),
    scripts=['script/run_pi_walk_slope', 'script/run_pi_joint', 'script/run_pi_gait', 'script/run_pi_emg'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6'],
    )
