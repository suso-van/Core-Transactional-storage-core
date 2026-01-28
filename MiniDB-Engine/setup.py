from setuptools import setup, find_packages

setup(
    name="minidb-engine",
    version="1.0.0.dev1",
    packages=find_packages(),
    install_requires=["pyyaml"],
    entry_points={
        "console_scripts": [
            "minidb=CLI.main:main"
        ]
    }
)
