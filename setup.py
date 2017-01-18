import re
import setuptools


setuptools.setup(
    name='char2font',
    version=re.search(r"__version__ *= *'([0-9]+\.[0-9]+\.[0-9]+)' *\n",
                      open('char2font/__init__.py').read()).group(1),
    description='Creates a dictionary of character to font image in JSON format.',
    long_description=open('README.md').read(),
    license='Public Domain',
    author='Yota Toyama',
    author_email='raviqqe@gmail.com',
    url='https://github.com/raviqqe/char2font.py/',
    packages=['char2font'],
    entry_points={
            'console_scripts': ['char2font=char2font.__main__:main']
    },
    install_requires=['docopt', 'numpy', 'pillow'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Fonts',
    ],
)
