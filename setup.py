from setuptools import setup, find_packages

setup(
    name="fmt-ts",
    description="Format typescript according to PEP-7",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "fmt-ts=fmt_ts._format_ts:main"
        ]
    }
)