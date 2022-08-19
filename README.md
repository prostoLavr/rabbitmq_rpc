# rabbitmq_rpc
## RabbitMq RPC lib

Setup:
```sh
# Copy
git clone https://github.com/prostoLavr/rabbitmq_rpc.git
cd rabbitmq_rpc
# Build
pip3 install wheel
python3 setup.py sdist bdist_wheel
# Install
pip3 install dist/rabbitmq_rpc-0.1-py3-none-any.whl
```

Use:
```python3
from rabbitmq_rpc import RpcClient  # Use on client
from rabbitmq_rpc import declare_to_recieve  # Use on server
```
