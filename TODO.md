Endpoints to be implemented:
- [x] GET instances
- [x] GET instance
- [x] POST instance (update), rename.
- [x] POST instance (create/launch) - start
  - [x]: Add `file_system_mounts` as param
  - [x]: Add `firewall_rulesets` as param
  - [x]: Add a `cheapest` flag? like with instance-types?
- [x] POST instance (terminate) - stop
- [x] POST instance (restart) - restart
- [x] GET instance types
- [x] GET keys
- [ ] POST keys (create)
- [ ] DELETE keys
- [ ] GET file-systems 
- [ ] DELETE file-system
- [x] GET images
- [ ] GET/PUT firewall-rules
- [ ] GET/POST firewall-rulesets
- [ ] GET/PATCH firewall-rulesets-global
- [ ] GET/PATCH/DELETE firewall-ruleset
- [ ] GET audit-events

Additional commands to be implemented:
- [x] lai ssh, ssh into an instance.
- [x] lai run --rm, start an instance, ssh into it, and optionally remove/turn-off the instance after exiting.

Improvements
- [x] Share auth_client globally so we can use the same thread when we need multiple calls. probably with @cached
- [x] Added run command
- [x] Added run env var arg
- [x] Added run volume arg
- [x] refactor instance type selection logic to me cleaner and return an InstanceType.
- [x] Starting an inference should tell you what it is starting, in which region and for what price.
- [x] Print API errors nicely.
- [ ] Should I be able to avoid regions? --exclude flag?
- [ ] Have a look at dry-run. I dislike that I have to pass it into start_instance. and why does run_cmd also have dry run?
- [ ] I'd like to exclude files/folders with .lambda-ai-ignore from volumes. Or should we introduce a .lambda-ai-api-client file?
- [ ] Rename user-data-file to cloud-init-file ?
- [ ] -w/--working-directory in run to cd to directory.
- [ ] add `lai rsync my-instance src:dst src:dst` or something similar so we can rsync from the command line. Potentially with --watch?
