from setuptools import setup, find_packages

with open('VERSION', 'r') as f:
    version = f.readline().strip()

setup(name='server',
      version=version,
      description="Sample server for multi-runtime",
      author='DaoCloud',
      url='http://www.daocloud.io',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
      ],
      )
