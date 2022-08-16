# rabbit_rpc
## RabbitMq RPC lib

Build:
```sh
cp path/to/lib
python setup.py sdist bdist_wheel
```

Use:
```python3
from rabbitmq_rpc import RpcClient  # Use on client
from rabbitmq_rpc import declare_to_recieve  # Use on server
```
