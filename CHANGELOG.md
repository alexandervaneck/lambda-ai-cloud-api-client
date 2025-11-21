# 2.0.0
* feat: Add `click` and refactor argparse.
* feat: Add `lai` command, as a shortcut to `lambda-ai`.
* feat: Add `lai ls` for displaying instances in a table.
* feat: Add `lai get` for display all information of an instance.
* feat: Add `lai start` for starting/launching new instances.
* feat: Add `lai stop` for stopping/terminating instances.
* feat: Add `lai restart` for restarting instances.
* feat: Add `lai images` for displaying images in a table.
* feat: Add `lai types` for displaying instance types in a table.
* feat: Add `lai keys` for displaying ssh keys in a table.
* removal: Remove lambda-ai command and instance-types, instances and ssh-keys subcommands. 

# 1.2.0
* docs: Set development status to production.

# 1.1.0
* feat: Rename `list` commands to `ls`.
* feat: Add `lambda-ai instance-types --available-only` to only list available instance types.
* feat: Add `lambda-ai instance-types --cheapest` to list the cheapest instance type.

# 1.0.0
* feat: Initial release.