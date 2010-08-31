from setuptools import setup, find_packages

setup(name='edw.repozos',
    version='0.2',
    author='Eau de Web',
    author_email='office@eaudeweb.ro',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={'console_scripts': [
        'do_backup = edw.repozos.backup:main',
        'do_cleanup = edw.repozos.cleanup:main',
    ]},
)
