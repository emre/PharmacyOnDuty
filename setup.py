from distutils.core import setup

setup(
    name='pharmacy_on_duty',
    version='0.0.1',
    packages=['pharmacy_on_duty'],
    url='https://github.com/emre/PharmacyOnDuty',
    license='MIT',
    author='emre',
    author_email='mail@emreyilmaz.me',
    description='Pharmacy On Duty API for Istanbul',
    entry_points={
        'console_scripts': [
            'fetch_pharmacy_data = pharmacy_on_duty.fetcher:update_pharmacy_info',
        ],
    },
)
