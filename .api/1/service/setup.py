from setuptools import setup, find_packages

setup(name='datastream_api_service',
      version='0.1.0',
      description="Datastream::API::Service",
      long_description="Datastream::API::Service",
      classifiers=[
        'Programming Language :: Python :: 3.9',
      ],
      keywords='datastream,api,service',
      url='https://dxnnymurphy.github.io',
      author="Danny Murphy",
      author_email='dannymurphy_7@icloud.com',
      license="MIT",
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      include_package_data=True,
      package_data={'': ['**/*.yml']},
      install_requires=[
        'click==8.1.3',
        'confluent-kafka==1.9.0',
        'elasticsearch==8.3.1',
        'environs==9.5.0',
        'flatdict==4.0.1',
        'google-api-python-client==2.57.0',
        'grpc-gateway-protoc-gen-openapiv2==0.1.0',
        'grpcio==1.47.0',
        'grpcio-reflection==1.47.0',
        'grpcio-tools==1.47.0',
        'pandas==1.4.3',
        'prometheus_client==0.14.1',
        'prometheus-kafka-metrics==0.4.2',
        'py-grpc-prometheus==0.7.0',
        #'pyspark==3.3.0',
        'python-dateutil==2.8.2',
        'pyyaml==6.0',
      ],
      entry_points={
        'console_scripts': [
          'datastream-api-service=kc.app.app:main',
        ]
      },
      cmdclass={},
      zip_safe=False)