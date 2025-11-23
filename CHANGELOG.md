# 2.2.1
* feat: Replace `lai ssh --ssh_ready_timeout_seconds` with the already existing `--timout-seconds`, and re-use.
* refactor: Remove SimpleNamespace as argument, this is a god-dict and not explicit enough.

# 2.2.0

* feat: `lai start` can now resolve instance type/region via filters (same as `lai types`) and supports `--dry-run` to
  show the planned launch without creating instances.

# 2.1.0

* feat: Add `lai ssh <name-or-id>` to ssh into a (starting) instance by name or id.
  This command will wait for an IP to be assigned and for port 22 to be available.

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
