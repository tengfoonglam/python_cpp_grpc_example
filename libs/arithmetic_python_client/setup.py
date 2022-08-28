from setuptools import setup

setup(name='arithmetic_python_client',
      author='Lam Teng Foong',
      author_email='tengfoonglam@yahoo.com.sg',
      description='Arithmetic Python Client',
      install_requires=["grpcio>=1.47.0", "grpcio-tools>=1.47.0", "protobuf>=3.19", "arithmetic_proto==0.0.0"],
      packages=["arithmetic_python_client"],
      zip_safe=False,
      python_requires=">=3.6")
