from setuptools import find_packages, setup

setup(
    name="genetic",
    packages=find_packages(include=["genetic"]),
    vesrion='0.0.1',
    description="A paradigm to use genetic algorithms",
    author="OmniThinker",
    install_requires=[],  # Where dependencies go
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.3.3'],
    test_suite='tests',
)
