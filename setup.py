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
        'markdown-inline-graphviz-extension'
    ]
)
