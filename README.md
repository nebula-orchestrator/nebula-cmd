# nebula-cmd

command line tool for managing nebula [nebula](http://nebula.readthedocs.io/en/latest/) clusters, only tested the CLI on Linux but should also work on Mac's.

refer to the [cmd](http://nebula.readthedocs.io/en/latest/cmd/) part of the guide in readthedocs for more details on how to use, --help is also an option as it's pretty self explanatory.

# quick walk-through
## install 

```bash
sudo wget https://github.com/nebula-orchestrator/nebula-cmd/raw/master/dist/nebulactl -O  /usr/local/bin/nebulactl && sudo chmod +x /usr/local/bin/nebulactl
```

## login

```bash
nebulactl login --username <root> --password <password> --host <nebula.host.com> --port <80> --protocol <http/https>
```

## use

```bash
nebulactl list
```
