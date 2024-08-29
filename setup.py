from setuptools import find_packages,setup

setup(
    name='question_generator',
    version='0.0.1',
    author='muttalip',
    author_email='sahilsheikh2187@gmail.com',
    install_requires=["langchain-community","langchain-google-genai","google-generativeai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)