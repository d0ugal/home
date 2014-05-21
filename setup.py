import ast
import codecs
import os

from setuptools import setup, find_packages


class VersionFinder(ast.NodeVisitor):
    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        if getattr(node.targets[0], 'id', None) == '__version__':
            self.version = node.value.s


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*parts):
    finder = VersionFinder()
    finder.visit(ast.parse(read(*parts)))
    return finder.version


setup(
    name="home",
    version=find_version("home", "__init__.py"),
    url='https://github.com/d0ugal/home',
    license='BSD',
    description="Home automation by @d0ugal.",
    long_description=read('README.rst'),
    author='Dougal Matthews',
    author_email='dougal@dougalmatthews.com',
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        'aiohttp>=0.7.2',
        'alembic>=0.6.4',
        'Flask-Admin>=1.0.7',
        'Flask-Login>=0.2.10',
        'Flask-Migrate>=1.2.0',
        'Flask-SQLAlchemy>=1.0',
        'Flask>=0.10.1',
        'psycopg2>=2.5.2',
        'python-dateutil>=2.2',
        'redis>=2.9.1',
        'rfxcom>=0.2.2',
        'simplejson>=3.3.3',
        'SQLAlchemy>=0.9.4',
        'uwsgi>=2.0',
    ],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'home = home.__main__:main'
        ]
    },
    zip_safe=False,
)
