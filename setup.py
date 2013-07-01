from distutils.core import setup
import os

_version_file_path = os.path.join(os.path.dirname(__file__), 'doctool/version.py')
with open(_version_file_path) as f:
    exec(f.read())

setup(
    name='doctool',
    version=__version__,
    packages=['doctool'],
    package_data={'doctool': ['style/*']},
    entry_points={
        'console_scripts': [
            'doctool = doctool.doctool:main'
        ]},
    install_requires=[
        'markdown==2.2.1',
        'jsontemplate',
        'python-markdown-graphviz'
    ],
    dependency_links=[
        'https://github.com/mikaellanger/python-markdown-graphviz/archive/master.tar.gz#egg=python-markdown-graphviz-master']
)
