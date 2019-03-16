import io

from setuptools import find_packages, setup

setup(
    name='shopper',
    version='0.1',
    url='localhost:5000',
    license='MIT',
    maintainer='Siddharth Sham',
    description='Online Shopping List generator',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
    },
)
