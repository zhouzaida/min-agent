from setuptools import find_packages, setup


setup(
    name='min_agent',
    version='0.1.0',
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=['openai', 'requests'],
)
