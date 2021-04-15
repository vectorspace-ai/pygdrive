from setuptools import setup

setup(
    name='pygdrive',
    version='1.0.0',
    packages=['pygdrive', 'pygdrive.tests'],
    url='https://github.com/vectorspace-ai/pygdrive',
    license='LICENSE',
    author='Arina Maltseva',
    author_email='arina@vectorspace.ai',
    description='Google Drive API for service accounts',
    long_description=open('README.md').read(),
    install_requires=[
        "google-api-python-client>=2.1.0",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=0.4.4",
    ],
)
