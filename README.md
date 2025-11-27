# Lambda Cloud API - CLI

This project is a wrapper around the Lambda Cloud API with some additional Quality-of-Life additions.
The documentation of the API can be found here: https://docs-api.lambda.ai/api/cloud

## Installation

```bash
uv pip install lambda-ai-cloud-api-client
```

## Usage

1. Set up an API token and environment.

In your lambda.ai account go to https://cloud.lambda.ai/api-keys/cloud-api and generate a new Cloud AI Key.
Set this token as an environment variable in the terminal you've installed this project.

```bash
export LAMBDA_CLOUD_API_TOKEN=<your-token>
```

The project also accepts `LAMBDA_CLOUD_TOKEN` and `LAMBDA_API_TOKEN` if you prefer that naming.
Optionally you can set the api base url, `LAMBDA_CLOUD_BASE_URL`, the default is https://cloud.lambdalabs.com .

2. Using the CLI

To save on keystrokes I've named the command `lai` for lambda.ai. To see all available commands use:

```bash
lai --help
```

## Overview of features

### Listing all instances

api doc: https://docs-api.lambda.ai/api/cloud#listInstances

```bash
lai ls
```

An overview of all your booting/running/terminating instances.

### Details of a single instance

api doc: https://docs-api.lambda.ai/api/cloud#getInstance

```bash
lai get <name-or-id>
```

### Starting an instance

api doc: https://docs-api.lambda.ai/api/cloud#launchInstance

Starting an instance with your configuration. You can choose to be exact and pass `--instance-type <your-type>` or use
filters that narrow to a single instance type.

```bash
lai start --instance-type gpu_1x_a10 --name my-instance --ssh-key my-ssh-key
```

or start the cheapest available instance with some hardware requirement.

```bash
lai start --cheapest --available --min-gpus 1 --name my-instance --ssh-key my-ssh-key
```

See `lai start --help` for all filters. They can be used all together to find the best instance type.
There's also a `--dry-run` option to see what would be selected.

### Restart an instance / instances

api doc: https://docs-api.lambda.ai/api/cloud#restartInstance

Restart an instance, multiple arguments are allowed.

```bash
lai restart <id-or-name. 
```

### Stop an instance / instances

api doc: https://docs-api.lambda.ai/api/cloud#terminateInstance

Stop an instance / instances, multiple arguments are allowed. This terminates the instance and removes it from your
inventory. You cannot restart/start terminated
instances.

```bash
lai stop <id-or-name> ...
```

### SSH into an instance

Finds an instance by id or name and then starts an ssh session to it. Handy if you want to stop copy+pasting IP
addresses of your started instances. Includes mechanism to wait for the instance to become available if it has just been
started.

```bash
lai ssh my-instance # or id
Waiting for IP on instance 'my-instance' (8ac73ac801a749099ed3bc2a5508000f)... retrying in 5s
Waiting for SSH on instance 'my-instance' (132.145.199.110)... retrying in 5s
Executing: ssh -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/dev/null ubuntu@132.145.199.110
(my-instance) $ 
```

### Running a command on an instance

Most of the time the workflow of using instances is:

1. Start an instance
2. Rsync your code to it.
3. Run a command, usually with env vars.
4. Rsync results back.
5. Stop the instance.

If this is your general workflow you'll find the following commands useful. In the most complex case it'll give you
access to spot-like instances where you only pay for the amount of time taken on a machine before it is shut down.

1. Run a command on an already started instance, including waiting for booting instances.

```bash
lai run my-instance -- <command>
```

2. Start an instance, then run the command.

```bash
lai run --cheapest --available --ssh-key my-ssh-key -- <command>
```

3. Start an instance, rsync a volume, run the cmd and rsync a volume back.

```bash
lai run --cheapest --available --ssh-key my-ssh-key -v <my-dir-or-file>:/home/ubuntu/ -- <command> /home/ubuntu/my-file
```

4. All of the above but delete the instance after done.

```bash
lai run --rm --cheapest --available --ssh-key my-ssh-key -v <my-dir-or-file>:/home/ubuntu/ -- <command> /home/ubuntu/my-file
```

### Listing instance types

api doc: https://docs-api.lambda.ai/api/cloud#listInstanceTypes

List all available instance types, with filters to select for `--available` or `--region`.

```bash
lai types
```

### Listing available boot images

api doc: https://docs-api.lambda.ai/api/cloud#listImages

List all available boot images, with filters to select `--arch` and `--family`.

```bash
lai images
```

### Listing your saved SSH keys

api doc: https://docs-api.lambda.ai/api/cloud#listSSHKeys

List all available ssh-keys you have saved in lambda.ai

```bash
lai keys
```
