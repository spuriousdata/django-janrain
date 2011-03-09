from setuptools import setup, find_packages

setup(
    name='django-janrain',
    version=".".join(map(str, __import__('janrain').__version__)),
    author=__import__('janrain').__author__,
    author_email='spuriousdata@gmail.com',
    description='Django integration of Janrain authentication system.',
    url='http://github.com/spuriousdata/django-janrain',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
)
