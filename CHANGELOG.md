# 2.3.0

* feat: Add `lai run <name-or-id> <command>` to run a command on a remote instance. Supports env vars.
* Breaking: CLI auth/options simplified (lambda_ai_cloud_api_client/__main__.py, cli/client.py)—removed
  --token/--base-url/--insecure; commands now read LAMBDA_CLOUD_TOKEN (and friends) plus optional
  LAMBDA_CLOUD_VERIFY_SSL, raising UsageError if missing/invalid.
* Breaking: CLI JSON outputs now emit parsed objects (print_json) instead of status-wrapped responses; commands like
  ls/get/start/stop/restart/run/types/images/keys return full instance/image/key/type dicts or render tables,
  so scripted consumers need to adjust.
* feat: HTTP failures now flow through Response.raise_for_status → HttpError → Click UsageError, improving
  user-facing error messages across the CLI.
* refactor: Instance lifecycle commands now resolve and display richer context—ssh/run show the chosen instance,
  enforce unique name/id matches, and surface timeouts for missing IP/SSH; start renders a launch plan table and
  ensures filters pick exactly one type/region.

# 2.2.1

* feat: Replace `lai ssh --ssh_ready_timeout_seconds` with the already existing `--timout-seconds`, and re-use.
* refactor: Remove SimpleNamespace as argument, this is a god-dict and not explicit enough.
* fix: Make Unset renderable by rich.

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
