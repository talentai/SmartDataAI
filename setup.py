from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smartdataai_test",
    version="4.2",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'statsmodels',
        'scipy',
        'scikit-learn',
        'langchain',
        'langchain-community',
        'langchain-core',
        'langchain-experimental',
        'langchain-openai'
    ],
    include_package_data=True,
    description='A package for SmartData management and operations.',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Ensure this is correct for Markdown
    author='Talent AI Now',
    author_email='contact@talentainow.com',
    url='https://github.com/yourusername/smartdataai',  # Update with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
