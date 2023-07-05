from setuptools import setup, 
setup(
	name='Tiendapeces',
	version='1.0.0b',
	license='GPLv3',
	author_email='jero98772@protonmail.com',
	author='jero98772',
	description='Online fish shop',
	packages=find_packages(),
    install_requires=['Django','crispy-bootstrap4','Pillow'],
    include_package_data=True,
)