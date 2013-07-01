from distutils.core import setup

with open("doctool/version.py") as f:
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
        'markdown',
        'jsontemplate',
        'python-markdown-graphviz'
    ],
    dependency_links=[
        'https://github.com/mikaellanger/python-markdown-graphviz/archive/master.tar.gz#egg=python-markdown-graphviz-master']
)
