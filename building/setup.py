from setuptools import setup, find_packages
 

requirements = ['pika']


setup(name='rabbitmq_rpc',
      version='0.1',
      url='https://github.com/prostolavr/rabbitmq_rpc',
      license='MIT',
      author='Lawrence Naumov',
      author_email='prostoLawr@gmail.com',
      packages=find_packages(),
      install_requires=requirements,
      classifiers=[
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      ],
      zip_safe=False)

