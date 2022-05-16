import io
import os

from setuptools import find_packages, setup

NAME = 'cojourn'
DESCRIPTION = 'A mock Flask API intended to be used with OpenHEMs'
URL = 'https://github.com/ACE-IoT-Solutions/cojourn'
AUTHOR = 'ACE IoT Solutions'
REQUIRES_PYTHON = '>=3.8.5'
VERSION = '0.1.0'

REQUIRED = [
    "click",
    "Flask",
    "Flask-JWT-Extended",
    "flask-restx",
    "PyJWT",
    "Werkzeug"
]

EXTRAS = {
}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    data_files=[("state", ["cojourn/state/example-state.json"])],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
)
