from setuptools import setup, find_packages
 

requirements = ['pika', 'loguru']


setup(name='rabbitmq_rpc',
      version='0.1.1',
      url='https://github.com/prostolavr/rabbitmq_rpc',
      author='Lawrence Naumov',
      author_email='prostoLawr@gmail.com',
      packages=find_packages(),
      install_requires=requirements,
      zip_safe=False)
