from setuptools import setup, find_packages

setup(
    name='Leo',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'pyaudio',
        'playsound',
        'numpy',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'start=openaileo:main',
        ],
    },
)
