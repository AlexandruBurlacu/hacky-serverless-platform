from setuptools import setup, find_packages

setup(name='libkvdb',
      version='0.4.6',
      packages=find_packages(),
      author="Alex Burlacu",
      author_email="alexburlacu1996@gmail.com",
      options={"bdist_wheel": {"universal": True}}
      )

