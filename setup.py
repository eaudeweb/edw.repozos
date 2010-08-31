from setuptools import setup, find_packages

setup(name='edw.repozos',
    version='0.1',
    author='Eau de Web',
    author_email='office@eaudeweb.ro',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={'console_scripts': ['do_repozos = edw.repozos.backup:main']},
)
