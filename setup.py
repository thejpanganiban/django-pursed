from setuptools import setup
import os


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()


setup(
    name="django-pursed",
    version="0.0.1",
    author="",
    author_email="",
    py_modules=['wallet', ],
    include_package_data=True,
    license='',  # 'GNU Library or Lesser General Public License (LGPL)',
    description="",
    long_description=README,
    url='',  # 'https://github.com/alej0varas/pypn',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='',
)
