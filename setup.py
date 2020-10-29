from distutils.core import setup

setup(
    name='pickdb',
    packages=['pickdb'],
    version='0.1',
    license='MIT',
    long_description=open('README.md', encoding='utf-8').read().replace('\n', ' '),
    long_description_content_type='text/markdown',
    description='A simple and easy database manager based on pickle.',
    author='Marino Iannarelli',
    author_email='marinoiannarelli97@gmail.com',
    url='https://github.com/Funpy97/pickdb',
    download_url='https://github.com/Funpy97/pickdb/archive/v0.1-alpha.tar.gz',
    keywords=['database', 'pickle', 'db'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
