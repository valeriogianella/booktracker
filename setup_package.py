from setuptools import setup, find_packages

setup(
    name="booktrack",
    version="1.0.0",
    description="A reading time tracking application",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "toga>=0.4.0",
    ],
    entry_points={
        "console_scripts": [
            "booktrack=booktrack.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
