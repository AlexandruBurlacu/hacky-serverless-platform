from setuptools import setup

setup(name='libkvdb',
      version='0.2.1',
      py_modules=['kvdb'],
      author="Alex Burlacu",
      author_email="alexburlacu1996@gmail.com",
      options={"bdist_wheel": {"universal": True}}
      )

