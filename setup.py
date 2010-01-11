from distutils.core import setup

setup(
    name='django-wsgi',
    version='0.1alpha1',
    description="A library for better integration between django and the WSGI world.",
    long_description=read('README.rst'),
    author='Alex Gaynor',
    author_email='alex.gaynor@gmail.com',
    license='BSD',
    url='http://github.com/alex/django-wsgi',
    py_modules=['django_wsgi'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
)
