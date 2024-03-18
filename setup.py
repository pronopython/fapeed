
from setuptools import setup

setup(name='fapeed',
	version='0.1.0-alpha',
	description='Fapeed - Adult Slideshow App',
	url='https://github.com/pronopython/fapeed',
	author='pronopython',
	author_email='pronopython@proton.me',
	license='GNU GENERAL PUBLIC LICENSE V3',
	packages=['fapeed'],
	package_data={'fapeed':['*']},
	include_package_data=True,
	zip_safe=False,
	install_requires=['pygame>=2.5.2','scipy>=1.12.0','numpy>=1.26.3','Pillow>=9.0.1','pyshortcuts>=1.9.0'],
	entry_points={
		'gui_scripts': [
			'fapeed_no_cli=fapeed.fapeed:main'
		],
        'console_scripts': [
            'fapeed_printModuleDir=fapeed.print_module_dir:printModuleDir',
            'fapeed=fapeed.fapeed:main'
		]
    	}
    )
