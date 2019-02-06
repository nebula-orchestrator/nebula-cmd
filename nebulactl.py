#!/usr/bin/env python2.7
import click, json, ast, os, base64
from NebulaPythonSDK import Nebula
from os.path import expanduser

VERSION = "2.0.1"


# i'm separating the nebulactl.py to 2 parts, the first is the NebulaCall class below which is going to be in charge of
# the communication with the SDK\API & formatting of replies to something a bit more CLI worthy
class NebulaCall:

    # the init step reads from the authfile, not keeping connection open as it's a CLI
    def __init__(self, ):
        try:
            home = expanduser("~")
            auth_file = open(home + "/.nebula.json", "r")
            auth_json = json.load(auth_file)
            self.connection = Nebula(username=auth_json["username"], password=base64.b64decode(auth_json["password"]),
                                     host=auth_json["host"], port=auth_json["port"], protocol=auth_json["protocol"])
        except Exception as e:
            click.echo(click.style(e, fg="red"))
            click.echo(click.style("error reading ~/nebula.json auth file, try logging in first", fg="red"))
            exit(2)

    def create_app(self, app, config):
        reply = self.connection.create_app(app, config)
        if reply["status_code"] == 200:
            click.echo(click.style("creating nebula app: " + app, fg="green"))
        elif reply["status_code"] == 400:
            click.echo(click.style("error creating " + app + ", missing or incorrect parameters", fg="red"))
        elif reply["status_code"] == 403:
            click.echo(click.style("error creating " + app + ", app already exist", fg="red"))
        else:
            click.echo(click.style("error creating " + app
                                   + ", are you logged in? did you sent the right params & app name?", fg="red"))

    def delete_app(self, app):
        reply = self.connection.delete_app(app)
        if reply["status_code"] == 200:
            click.echo(click.style("deleting nebula app: " + app, fg="magenta"))
        elif reply["status_code"] == 403:
            click.echo(click.style("error deleting " + app + ", app doesn't exist", fg="red"))
        else:
            click.echo(click.style("error deleting " + app
                                   + ", are you logged in? did you sent the right app name?", fg="red"))

    def list_apps(self):
        reply = self.connection.list_apps()
        if reply["status_code"] == 200:
            reply_json = reply["reply"]
            if len(reply_json["apps"]) == 0:
                click.echo("no apps in nebula cluster")
            else:
                click.echo("nebula cluster apps:")
                for app in reply_json["apps"]:
                    click.echo(app)
        else:
            click.echo(
                click.style(
                    "error retuning list of nebula apps, are you logged in?",
                    fg="red"))

    def check_api(self):
        reply = self.connection.check_api()
        if reply["status_code"] == 200:
            reply_json = reply["reply"]
            if reply_json == {'api_available': True}:
                click.echo("nebula responding as expected")
            else:
                click.echo(
                    click.style(
                        "nebula api not responding, are you logged in?",
                        fg="red"))
        else:
            click.echo(
                click.style(
                    "nebula api not responding, are you logged in?",
                    fg="red"))

    def list_app_info(self, app):
        reply = self.connection.list_app_info(app)
        reply_json = reply["reply"]
        if reply["status_code"] == 200:
            for key, value in reply_json.items():
                click.echo(str(key) + ": " + json.dumps(value))
        else:
            click.echo(click.style("error listing " + app
                                   + " info, are you logged in? did you sent the right app name?", fg="red"))

    def stop_app(self, app):
        reply = self.connection.stop_app(app)
        if reply["status_code"] == 202:
            click.echo("stopping nebula app: " + app)
        else:
            click.echo(click.style("error stopping " + app +
                                   ", are you logged in? did you sent the right app name?", fg="red"))

    def start_app(self, app):
        reply = self.connection.start_app(app)
        if reply["status_code"] == 202:
            click.echo("starting nebula app: " + app)
        else:
            click.echo(click.style("error starting " + app
                                   + ", are you logged in? did you sent the right app name?", fg="red"))

    def restart_app(self, app):
        reply = self.connection.restart_app(app)
        if reply["status_code"] == 202:
            click.echo(click.style("restarting nebula app: " + app, fg="yellow"))
        else:
            click.echo(click.style("error restarting " + app
                                   + ", are you logged in? did you sent the right app name?", fg="red"))

    def update_app(self, app, config):
        reply = self.connection.update_app(app, config)
        if reply["status_code"] == 202:
            click.echo("updating nebula app: " + app)
        elif reply["status_code"] == 400:
            click.echo(click.style("error updating " + app + ", missing or incorrect parameters", fg="red"))
        else:
            click.echo(click.style("error updating " + app
                                   + ", are you logged in? did you sent the right params & app name?", fg="red"))

    def prune_device_group_images(self, app):
        reply = self.connection.prune__device_group_images(app)
        if reply["status_code"] == 202:
            click.echo(click.style("pruning images on devices running app: " + app, fg="yellow"))
        else:
            click.echo(click.style("error pruning images on devices running app:" + app
                                   + ", are you logged in? did you sent the right app name?", fg="red"))

    def prune_images(self):
        reply = self.connection.prune_images()
        if reply["status_code"] == 202:
            click.echo(click.style("pruning images on all devices", fg="yellow"))
        else:
            click.echo(click.style("error pruning images on all devices, are you logged in? did you sent the "
                                   "right app name?", fg="red"))

    def list_device_group(self, device_group):
        reply = self.connection.list_device_group(device_group)
        reply_json = reply["reply"]
        if reply["status_code"] == 200:
            for key, value in reply_json.items():
                click.echo(str(key) + ": " + json.dumps(value))
        else:
            click.echo(click.style("error listing device_group :" + device_group
                                   + ", are you logged in? did you sent the right device_group name?", fg="red"))

    def list_device_groups(self):
        reply = self.connection.list_device_groups()
        reply_json = reply["reply"]
        if reply["status_code"] == 200:
            for key, value in reply_json.items():
                click.echo(str(key) + ": " + json.dumps(value))
        else:
            click.echo(click.style("error listing device_groups, are you logged in?", fg="red"))

    def delete_device_group(self, device_group):
        reply = self.connection.delete_device_group(device_group)
        if reply["status_code"] == 200:
            click.echo(click.style("deleted device_group " + device_group, fg="red"))
        else:
            click.echo(click.style("error listing device_group :" + device_group
                                   + ", are you logged in? did you sent the right device_group name?", fg="red"))

    def create_device_group(self, device_group, config):
        reply = self.connection.create_device_group(device_group, config)
        if reply["status_code"] == 200:
            click.echo(click.style("creating nebula device_group: " + device_group, fg="green"))
        elif reply["status_code"] == 400:
            click.echo(click.style("error creating " + device_group + ", missing or incorrect parameters", fg="red"))
        elif reply["status_code"] == 403:
            click.echo(click.style("error creating " + device_group + ", device_group already exist", fg="red"))
        else:
            click.echo(click.style("error creating " + device_group
                                   + ", are you logged in? did you sent the right params & app name?", fg="red"))

    def update_device_group(self, device_group, config):
        reply = self.connection.update_device_group(device_group, config)
        if reply["status_code"] == 202:
            click.echo(click.style("updating nebula device_group: " + device_group, fg="green"))
        elif reply["status_code"] == 400:
            click.echo(click.style("error updating " + device_group + ", missing or incorrect parameters", fg="red"))
        elif reply["status_code"] == 403:
            click.echo(click.style("error updating " + device_group + ", device_group already exist", fg="red"))
        else:
            click.echo(click.style("error updating " + device_group
                                   + ", are you logged in? did you sent the right params & app name?", fg="red"))


# the 2nd part of nebulactl.py, the click functions from here until the end of the file are in charge of the CLI side of
# things, meaning help text, arguments input, arguments prompts & login file interfacing
@click.version_option(version=VERSION)
@click.group(help="Connect to a Nebula orcherstrator management endpoint, Create Nebula apps and Manage them all from "
                  "a simple CLI.")
def nebulactl():
    pass


# command group for everything image pruning related
@click.version_option(version=VERSION)
@nebulactl.group(help="Prune images.")
def prune():
    pass


# command group for everything app related
@click.version_option(version=VERSION)
@nebulactl.group(help="Manage nebula apps.")
def apps():
    pass


# command group for everything device_group related
@click.version_option(version=VERSION)
@nebulactl.group(help="Manage nebula device_groups.")
def device_groups():
    pass


# creates a cred file at ~/.nebula.json with the auth credentials or updates it's values if it exists
@nebulactl.command(help="login to nebula")
@click.option('--username', '-u', prompt='what is nebula manager basic auth username?',
              help='nebula manager basic auth username')
@click.option('--password', '-p', prompt='what is nebula manager basic auth password?', hide_input=True,
              confirmation_prompt=True, help='nebula manager basic auth password')
@click.option('--host', '-h', prompt='what is nebula manager host?', help='nebula manager host.')
@click.option('--port', '-c', prompt='what is nebula manager port?', help='nebula manager port, defaults to 80',
              default=80, type=click.IntRange(1, 65535))
@click.option('--protocol', '-P', prompt='what is nebula manager protocol?', default="http",
              help='nebula manager protocol, defaults to http')
def login(username, password, host, port, protocol):
    home = expanduser("~")
    auth_file = open(home + "/.nebula.json", "w+")
    json.dump({"username": username, "password": base64.b64encode(password), "host": host, "port": port,
               "protocol": protocol}, auth_file)
    auth_file.write('\n')


# deletes the cred file from the user home folder
@nebulactl.command(help="logout of nebula, useful when you want to make sure to delete stored credentials")
def logout():
    home = expanduser("~")
    os.remove(home + "/.nebula.json", )


@nebulactl.command(help="check nebula api responds")
def ping():
    connection = NebulaCall()
    connection.check_api()


@apps.command(help="list nebula apps", name="list")
def list_apps():
    connection = NebulaCall()
    connection.list_apps()


# create requires all the params so prompting for everything that missing with sensible\empty defaults where possible
@apps.command(help="create a new nebula app", name="create")
@click.option('--app', '-a', help='nebula app name to create', prompt='what is nebula app name to create?')
@click.option('--starting_ports', '-p', prompt="what are the app starting ports?", default=[],
              help='starting ports to run in the format of X:Y,A:B where X,A=host_port & Y,B=container_port')
@click.option('--containers_per', '-c', prompt="what are the app containers_per value?",
              help='cpu:X or server:X where X is the number of containers per cpu or server to have')
@click.option('--env_vars', '-e', help='nebula app envvars in the format of key:value,key1:value1... defaults to none',
              prompt="what are the app envvars?")
@click.option('--image', '-i', help='nebula app docker image', prompt="what is the app docker image?")
@click.option('--running/--stopped', '-r/-s', default=True, help='nebula app running/stopped state, defaults to True',
              prompt="should the app start in the running state?")
@click.option('--networks', '-n', default="", prompt="what is the app networks?",
              help='nebula app network mode in csv format, defaults to [] ("nebula")')
@click.option('--volumes', '-v', default=[], prompt="what is the app volume mounts?",
              help='nebula app volume mounts in csv format, defaults to [] (none/empty)')
@click.option('--devices', '-d', default=[], prompt="what is the app devices mounts?",
              help='nebula app devices mounts in csv format, defaults to [] (none/empty)')
@click.option('--privileged/--unprivileged', '-P/-U', default=False,
              help='nebula app privileged state, defaults to False',
              prompt="should the app start with privileged permissions?")
@click.option('--rolling/--restart', '-R/-S', default=False, help='nebula app rolling restart/normal restart state',
              prompt="should the app roll or restart normally?")
def create_app(app, starting_ports, containers_per, env_vars, image, running, networks, volumes, devices, privileged,
               rolling):
    starting_ports = starting_ports.split(",")
    ports_list = []
    for ports in starting_ports:
        ports = ports.split(":")
        ports_dict = {str(ports[0]): str(ports[1])}
        ports_list.append(ports_dict)
    containers_per = str(containers_per).split(":")
    containers_per_dict = {containers_per[0]: int(containers_per[1])}
    if volumes is not []:
        volumes = volumes.split(",")
    if networks is not []:
        networks = networks.split(",")
    env_vars = ast.literal_eval("{\"" + env_vars.replace(":", "\":\"").replace(",", "\",\"") + "\"}")
    config_json = {"starting_ports": ports_list, "containers_per": containers_per_dict,
                   "env_vars": dict(env_vars), "docker_image": str(image), "running": bool(running),
                   "networks": networks, "volumes": volumes, "devices": devices,
                   "privileged": bool(privileged), "rolling_restart": bool(rolling)}
    connection = NebulaCall()
    connection.create_app(app, config_json)


@apps.command(help="delete a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to delete?', help='nebula app name to delete')
@click.confirmation_option(help='auto confirm you want to delete the app',
                           prompt="are you sure you want to delete? there is no restore option")
def delete(app):
    connection = NebulaCall()
    connection.delete_app(app)


@apps.command(help="list info of a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to get info of?', help='nebula app name to get info of')
def info(app):
    connection = NebulaCall()
    connection.list_app_info(app)


@apps.command(help="start a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to start?', help='nebula app name to start')
def start(app):
    connection = NebulaCall()
    connection.start_app(app)


@apps.command(help="stop a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to stop?', help='nebula app name to stop')
def stop(app):
    connection = NebulaCall()
    connection.stop_app(app)


@apps.command(help="restart a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to restart?', help='nebula app name to restart')
def restart(app):
    connection = NebulaCall()
    connection.restart_app(app)


# update can be any combination of params, only one that's 100% required is the --app so it's the only one i'm prompting
@apps.command(help="update a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to update?', help='nebula app name to update')
@click.option('--starting_ports', '-p',
              help='starting ports to run in the format of X:Y,A:B where X,A=host_port & Y,B=container_port')
@click.option('--containers_per', '-c',
              help='cpu:X or server:X where X is the number of containers per cpu or server to have')
@click.option('--env_vars', '-e', help='nebula app envvars in the format of key:value,key1:value1...')
@click.option('--image', '-i', help='nebula app docker image')
@click.option('--running/--stopped', '-r/-s', help='nebula app running/stopped state')
@click.option('--networks', '-n', help='nebula app network mode in csv format')
@click.option('--volumes', '-v', help='nebula app volume mounts in csv format')
@click.option('--devices', '-d', help='nebula app devices mounts in csv format, defaults to [] (none/empty)')
@click.option('--privileged/--unprivileged', '-P/-U', help='nebula app privileged state, defaults to False')
@click.option('--rolling/--restart', '-R/-S', help='nebula app rolling restart/normal restart state')
def update(app, starting_ports, containers_per, env_vars, image, running, networks, volumes, devices, privileged,
           rolling):
    config_json = {}
    if starting_ports is not None:
        starting_ports = starting_ports.split(",")
        ports_list = []
        for ports in starting_ports:
            ports = ports.split(":")
            ports_dict = {str(ports[0]): str(ports[1])}
            ports_list.append(ports_dict)
        config_json["starting_ports"] = ports_list
    if containers_per is not None:
        containers_per = str(containers_per).split(":")
        containers_per_dict = {containers_per[0]: int(containers_per[1])}
        config_json["containers_per"] = containers_per_dict
    if env_vars is not None:
        env_vars = ast.literal_eval("{\"" + env_vars.replace(":", "\":\"").replace(",", "\",\"") + "\"}")
        config_json["env_vars"] = dict(env_vars)
    if image is not None:
        config_json["docker_image"] = str(image)
    if running is not None:
        config_json["running"] = bool(running)
    if rolling is not None:
        config_json["rolling_restart"] = bool(rolling)
    if networks is not None:
        if networks != '[]':
            networks = networks.split(",")
            config_json["networks"] = networks
        elif networks == '[]':
            config_json["networks"] = []
    if devices is not None:
        if devices != '[]':
            devices = devices.split(",")
            config_json["devices"] = devices
        elif devices == '[]':
            config_json["devices"] = []
    if privileged is not None:
        config_json["privileged"] = bool(privileged)
    if volumes is not None:
        if volumes != '[]':
            volumes = volumes.split(",")
            config_json["volumes"] = volumes
        elif volumes == '[]':
            config_json["volumes"] = []

    connection = NebulaCall()
    connection.update_app(app, config_json)


@device_groups.command(help="list a device_group", name="info")
@click.option('--device_group', '-d', help='nebula device_group to get config of',
              prompt='what is the device_group name?')
def device_group_info(device_group):
    connection = NebulaCall()
    connection.list_device_group(device_group)


@device_groups.command(help="list all device_groups", name="list")
def list_all_device_groups():
    connection = NebulaCall()
    connection.list_device_groups()


@prune.command(help="prune unused images on a device_group", name="device_group")
@click.option('--device_group', '-d', help='nebula device_group to prune images on',
              prompt='what is the device_group name on devices you want to prune unused images on?')
def prune_device_group(device_group):
    connection = NebulaCall()
    connection.prune_device_group_images(device_group)


@prune.command(help="prune unused images on all device_groups", name="all")
def prune_all():
    connection = NebulaCall()
    connection.prune_images()


@device_groups.command(help="delete a device_group", name="delete")
@click.option('--device_group', '-d', help='nebula device_group to delete', prompt='what is the device_group name?')
@click.confirmation_option(help='auto confirm you want to delete the device_group',
                           prompt="are you sure you want to delete? there is no restore option")
def device_group_delete(device_group):
    connection = NebulaCall()
    connection.delete_device_group(device_group)


@device_groups.command(help="create a new nebula device_group", name="create")
@click.option('--device_group', '-d', help='nebula device_group to create', prompt='what is the device_group name?')
@click.option('--apps', '-a', prompt="what are the device_group apps?",
              help='a CSV list of the apps that are part of the device_group')
def device_group_create(device_group, apps):
    apps_list = apps.split(",")
    config_json = {"apps": apps_list}
    connection = NebulaCall()
    connection.create_device_group(device_group, config_json)


@device_groups.command(help="update a new nebula device_group", name="update")
@click.option('--device_group', '-d', help='nebula device_group to update', prompt='what is the device_group name?')
@click.option('--apps', '-a', prompt="what are the device_group apps?",
              help='a CSV list of the apps that are part of the device_group')
def device_group_update(device_group, apps):
    apps_list = apps.split(",")
    config_json = {"apps": apps_list}
    connection = NebulaCall()
    connection.update_device_group(device_group, config_json)


if __name__ == '__main__':
    nebulactl()
