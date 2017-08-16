#!/usr/bin/env python2.7
import click, json, ast, os
from NebulaPythonSDK import Nebula
from os.path import expanduser


VERSION = "1.0.1"


# i'm separating the nebulactl.py to 2 parts, the first is the NebulaCall class below which is going to be in charge of
# the communication with the SDK\API & formatting of replies to something a bit more CLI worthy
class NebulaCall:

    # the init step reads from the authfile, not keeping connection open as it's a CLI
    def __init__(self,):
        try:
            home = expanduser("~")
            auth_file = open(home + "/.nebula.json", "r")
            auth_json = json.load(auth_file)
            self.connection = Nebula(username=auth_json["username"], password=auth_json["password"],
                                     host=auth_json["host"], port=auth_json["port"], protocol=auth_json["protocol"])
        except:
            click.echo(click.style("error reading ~/nebula.json auth file, try logging in first", fg="red"))
            exit(2)

    def create_app(self, app, config):
        reply = self.connection.create_app(app, config)
        if reply.status_code == 202:
            click.echo(click.style("creating nebula app: " + app, fg="green"))
        elif reply.status_code == 400:
            click.echo(click.style("error creating " + app + ", missing\incorrect parameters", fg="red"))
        elif reply.status_code == 403:
            click.echo(click.style("error creating " + app + ", app already exist", fg="red"))
        else:
            click.echo(click.style("error creating " + app
                                   + ", are you logged in? did you sent the right params & app name?", fg="red"))

    def delete_app(self, app):
        reply = self.connection.delete_app(app)
        if reply.status_code == 202:
            click.echo(click.style("deleting nebula app: " + app, fg="magenta"))
        elif reply.status_code == 403:
            click.echo(click.style("error deleting " + app + ", app doesn't exist", fg="red"))
        else:
            click.echo(click.style("error deleting " + app
                                   + ", are you logged in? did you sent the right app name?", fg="red"))

    def list_apps(self):
        reply = self.connection.list_apps()
        if reply.status_code == 200:
            reply_json = reply.json()
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
        if reply.status_code == 200:
            reply_json = reply.json()
            if reply_json == {'api_available': 'True'}:
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
        reply_json = reply.json()
        if reply.status_code == 200:
            for key, value in reply_json.items():
                click.echo(str(key) + ": " + json.dumps(value))
        else:
            click.echo(click.style("error listing " + app
                                   + " info, are you logged in? did you sent the right app name?", fg="red"))

    def stop_app(self, app):
        reply = self.connection.stop_app(app)
        if reply.status_code == 202:
            click.echo("stopping nebula app: " + app)
        else:
            click.echo(click.style("error stopping " + app +
                                   ", are you logged in? did you sent the right app name?", fg="red"))

    def start_app(self, app):
        reply = self.connection.start_app(app)
        if reply.status_code == 202:
            click.echo("starting nebula app: " + app)
        else:
            click.echo(click.style("error starting " + app
                                   + ", are you logged in? did you sent the right app name?", fg="red"))

    def restart_app(self, app):
        reply = self.connection.restart_app(app)
        if reply.status_code == 202:
            click.echo(click.style("restarting nebula app: " + app, fg="yellow"))
        else:
            click.echo(click.style("error restarting " + app
                                   + ", are you logged in? did you sent the right app name?", fg="red"))

    def update_app(self, app, config):
        reply = self.connection.update_app(app, config)
        if reply.status_code == 202:
            click.echo("updating nebula app: " + app)
        elif reply.status_code == 400:
            click.echo(click.style("error updating " + app + ", missing\incorrect parameters", fg="red"))
        else:
            click.echo(click.style("error updating " + app
                                   + ", are you logged in? did you sent the right params & app name?", fg="red"))

    def roll_app(self, app):
        reply = self.connection.roll_app(app)
        if reply.status_code == 202:
            click.echo(click.style("rolling nebula app: " + app, fg="yellow"))
        else:
            click.echo(click.style("error rolling " + app
                                   + ", are you logged in? did you sent the right app name?", fg="red"))


# the 2nd part of nebulactl.py, the click functions from here until the end of the file are in charge of the CLI side of
# things, meaning help text, arguments input, arguments prompts & login file interfacing
@click.version_option(version=VERSION)
@click.group(help="manage a nebula cluster")
def nebulactl():
    pass


# creates a cred file at ~/.nebula.json with the auth credentials or updates it's values if it exists
@nebulactl.command(help="login to nebula")
@click.option('--username', '-u', prompt='what is nebula api-manager basic auth username?',
              help='nebula api-manager basic auth username')
@click.option('--password', '-p', prompt='what is nebula api-manager basic auth password?', hide_input=True,
              confirmation_prompt=True, help='nebula api-manager basic auth password')
@click.option('--host', '-h', prompt='what is nebula api-manager host?', help='nebula api-manager host.')
@click.option('--port', '-c', prompt='what is nebula api-manager port?', help='nebula api-manager port, defaults to 80',
              default=80, type=click.IntRange(1, 65535))
@click.option('--protocol', '-P', prompt='what is nebula api-manager protocol?', default="http",
              help='nebula api-manager protocol, defaults to http')
def login(username, password, host, port, protocol):
    home = expanduser("~")
    auth_file = open(home + "/.nebula.json", "w+")
    json.dump({"username": username, "password": password, "host": host, "port": port, "protocol": protocol}, auth_file)
    auth_file.write('\n')


# deletes the cred file from the user home folder
@nebulactl.command(help="logout of nebula, useful when you want to make sure to delete stored credentials")
def logout():
    home = expanduser("~")
    os.remove(home + "/.nebula.json",)


@nebulactl.command(help="list nebula apps")
def list():
    connection = NebulaCall()
    connection.list_apps()


@nebulactl.command(help="check nebula api responds")
def ping():
    connection = NebulaCall()
    connection.check_api()


# create requires all the params so prompting for everything that missing with sensible\empty defaults where possible
@nebulactl.command(help="create a new nebula app")
@click.option('--app', '-a', help='nebula app name to create',  prompt='what is nebula app name to create?')
@click.option('--starting_ports', '-p', prompt="what are the app starting ports?", default=[],
              help='starting ports to run in the format of X:Y,A:B where X,A=host_port & Y,B=container_port')
@click.option('--containers_per', '-c', prompt="what are the app containers_per value?",
              help='cpu:X or server:X where X is the number of containers per cpu\server to have')
@click.option('--env_vars', '-e', help='nebula app envvars in the format of key:value,key1:value1... defaults to none',
              prompt="what are the app envvars?")
@click.option('--image', '-i', help='nebula app docker image', prompt="what is the app docker image?")
@click.option('--running', '-r', default=True, help='nebula app running/stopped state, defaults to True',
              prompt="should the app start in the running state?")
@click.option('--network_mode', '-n', default="bridge", prompt="what is the app network_mode?",
              help='nebula app network mode (host, bridge, etc...), defaults to bridge')
@click.option('--volumes', '-v', default=[], prompt="what is the app volume mounts?",
              help='nebula app volume mounts in csv format, defaults to [] (none/empty)')
@click.option('--devices', '-d', default=[], prompt="what is the app devices mounts?",
              help='nebula app devices mounts in csv format, defaults to [] (none/empty)')
@click.option('--privileged', '-P', default=False, help='nebula app privileged state, defaults to False',
              prompt="should the app start with privileged permissions?")
def create(app, starting_ports, containers_per, env_vars, image, running, network_mode, volumes, devices, privileged):
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
    env_vars = ast.literal_eval("{\"" + env_vars.replace(":", "\":\"").replace(",", "\",\"") + "\"}")
    config_json = {"starting_ports": ports_list, "containers_per": containers_per_dict,
                   "env_vars": dict(env_vars), "docker_image": str(image), "running": bool(running),
                   "network_mode": str(network_mode), "volumes": volumes, "devices": devices,
                   "privileged": bool(privileged)}
    connection = NebulaCall()
    connection.create_app(app, config_json)


@nebulactl.command(help="delete a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to delete?', help='nebula app name to delete')
@click.confirmation_option(help='auto confirm you want to delete the app',
                           prompt="are you sure you want to delete? there is no restore option")
def delete(app):
    connection = NebulaCall()
    connection.delete_app(app)


@nebulactl.command(help="list info of a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to get info of?', help='nebula app name to get info of')
def info(app):
    connection = NebulaCall()
    connection.list_app_info(app)


@nebulactl.command(help="start a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to start?', help='nebula app name to start')
def start(app):
    connection = NebulaCall()
    connection.start_app(app)


@nebulactl.command(help="stop a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to stop?', help='nebula app name to stop')
def stop(app):
    connection = NebulaCall()
    connection.stop_app(app)


@nebulactl.command(help="restart a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to restart?', help='nebula app name to restart')
def restart(app):
    connection = NebulaCall()
    connection.restart_app(app)


# update can be any combination of params, only one that's 100% required is the --app so it's the only one i'm prompting
@nebulactl.command(help="update a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to update?', help='nebula app name to update')
@click.option('--starting_ports', '-p',
              help='starting ports to run in the format of X:Y,A:B where X,A=host_port & Y,B=container_port')
@click.option('--containers_per', '-c',
              help='cpu:X or server:X where X is the number of containers per cpu\server to have')
@click.option('--env_vars', '-e', help='nebula app envvars in the format of key:value,key1:value1...')
@click.option('--image', '-i', help='nebula app docker image')
@click.option('--running', '-r', help='nebula app running/stopped state')
@click.option('--network_mode', '-n', help='nebula app network mode (host, bridge, etc...)')
@click.option('--volumes', '-v', help='nebula app volume mounts in csv format')
@click.option('--devices', '-d', help='nebula app devices mounts in csv format, defaults to [] (none/empty)')
@click.option('--privileged', '-P', help='nebula app privileged state, defaults to False')
def update(app, starting_ports, containers_per, env_vars, image, running, network_mode, volumes, devices, privileged):
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
    if network_mode is not None:
        config_json["network_mode"] = str(network_mode)
    if devices is not None:
        if devices != '[]':
            devices = volumes.split(",")
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


@nebulactl.command(help="rolling restart a nebula apps")
@click.option('--app', '-a', prompt='what is nebula app name to rolling restart?',
              help='nebula app name to rolling restart')
def roll(app):
    connection = NebulaCall()
    connection.roll_app(app)


if __name__ == '__main__':
    nebulactl()
