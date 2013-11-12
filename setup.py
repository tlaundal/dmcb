from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')

setup(
    name='dmcb',
    version='1.0',
    long_description='Dynamic Minecraft Banner',
    packages=['dmcb'],
    include_package_data=True,
    zip_safe=False,
    dependency_links=[str(req_line.url) for req_line in install_reqs],
    install_requires=[str(ir.req) for ir in install_reqs if not ir.req == None]
)
