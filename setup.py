import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = "0.0.1"
PACKAGE_NAME = "fast_alchemy_models"
AUTHOR = "Ludens productions"
AUTHOR_EMAIL = "ludens@ludensproductions.com"
URL = "https://github.com/ludensproductions/"

LICENSE = "MIT"
DESCRIPTION = "Mixin utilities for sqlalchemy models"
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf-8")
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    "sqlalchemy_mixins >= 2.0.5",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
)
