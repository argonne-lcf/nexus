# Compute Endpoints
Here we have sample configurations for Globus Compute endpoints for ALCF machines.

Details on how to setup a Globus Compute endpoint can be found [here](https://funcx.readthedocs.io/en/latest/endpoints.html).

Templates for ALCF machines:
- [polaris-gpu-config.yaml](polaris-gpu-config.yaml): an endpoint config that will set up 4 workers per node and assign 1 gpu and 4 cpu hardware threads per worker.
- [polaris-cpu-config.yaml](polaris-cpu-config.yaml): an endpoint config that will setup 32 workers per node and assign 1 cpu core per worker

To use a template first edit it to include your project name, initialization commands, etc.  Then to configure the endpoint:

```bash
globus-compute-endpoint configure --endpoint-config config_template.yaml my_endpoint
globus-compute-endpoint start my_endpoint
```

Note that endpoints will need to be reactivated after machine maintenance days but may also become unstable at other times and need to be restarted.
