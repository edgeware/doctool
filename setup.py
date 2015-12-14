from distutils.core import setup

setup(
    name='doctool',
    version=0.7,
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
        'https://github.com/edgeware/python-markdown-graphviz/archive/master.tar.gz#egg=python-markdown-graphviz']
)
