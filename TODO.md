Endpoints to be implemented:
- [x] GET instances
- [x] GET instance
- [x] POST instance (update), rename.
- [x] POST instance (create/launch) - start
  - [ ]: Add `file_system_mounts` as param
  - [ ]: Add `firewall_rulesets` as param
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
- [ ] lai run --rm, start an instance, ssh into it, and optionally remove/turn-off the instance after exiting.
