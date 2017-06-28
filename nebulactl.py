#!/usr/bin/env python2.7
import click, json
from NebulaPythonSDK import Nebula
from os.path import expanduser


VERSION = "0.8.1"


class NebulaCall:

    def __init__(self,):
        try:
            home = expanduser("~")
            auth_file = open(home + "/.nebula.json", "r")
            auth_json = json.load(auth_file)
            self.connection = Nebula(username=auth_json["username"], password=auth_json["password"],
                                     host=auth_json["host"], port=auth_json["port"], protocol=auth_json["protocol"])
        except:
            print "error reading ~/nebula.json auth file, try logging in first"
            exit(2)

    def create_app(self, app, config):
        # todo - print a real reply
        print self.connection.create_app(app, config).text

    def delete_app(self, app):
        reply = self.connection.delete_app(app)
        if reply.status_code == 202:
            print "deleting nebula app: " + app
        elif reply.status_code == 403:
            print "error deleting " + app + ", app doesn't exist"
        else:
            print "error deleting " + app + ", are you sure you logged in with the correct information?"

    def list_apps(self):
        reply = self.connection.list_apps()
        if reply.status_code == 200:
            reply_json = reply.json()
            if len(reply_json["apps"]) == 0:
                print "no apps in nebula cluster"
            else:
                print "nebula cluster apps:"
                for app in reply_json["apps"]:
                    print app
        else:
            print "error retuning list of nebula apps, are you sure you logged in with the correct information?"

    def list_app_info(self, app):
        reply = self.connection.list_app_info(app)
        reply_json = reply.json()
        if reply.status_code == 200:
            for key, value in reply_json.items():
                print str(key) + ": " + json.dumps(value)
        else:
            print "error listing " + app + " info, are you sure you logged in with the correct information?"

    def stop_app(self, app):
        reply = self.connection.stop_app(app)
        if reply.status_code == 202:
            print "stopping nebula app: " + app
        else:
            print "error stopping " + app + ", are you sure you logged in with the correct information?"

    def start_app(self, app):
        reply = self.connection.start_app(app)
        if reply.status_code == 202:
            print "starting nebula app: " + app
        else:
            print "error starting " + app + ", are you sure you logged in with the correct information?"

    def restart_app(self, app):
        reply = self.connection.restart_app(app)
        if reply.status_code == 202:
            print "restarting nebula app: " + app
        else:
            print "error restarting " + app + ", are you sure you logged in with the correct information?"

    def update_app(self, app, config):
        # todo - print a real reply
        print self.connection.update_app(app, config).text

    def roll_app(self, app):
        reply = self.connection.roll_app(app)
        if reply.status_code == 202:
            print "rolling nebula app: " + app
        else:
            print "error rolling " + app + ", are you sure you logged in with the correct information?"


@click.version_option(version=VERSION)
@click.group(help="manage a nebula cluster")
def nebulactl():
    pass


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


@nebulactl.command(help="list nebula apps")
def list():
    connection = NebulaCall()
    connection.list_apps()


# todo - half cooked, need to get this working but too tired/pissed to think straight right now
@nebulactl.command(help="create a new nebula app")
@click.option('--app', '-a', help='nebula app name to create',  prompt='what is nebula app name to create?')
@click.option('--starting_ports', '-p', prompt="what are the app starting ports?", default=[],
              help='starting ports to run in the format of [{"X": "Y"}, Z, ... ] where x=host_port & Y=container_port '
                   '& Z is shorthand for writing "Z": "Z"')
@click.option('--containers_per', '-c', prompt="what are the app containers_per value?",
              help='{cpu:X} or {server:X} where X is the number of containers per cpu\server to have')
@click.option('--env_vars', '-e', help='nebula app envvars in the format of key:value, defaults to none',
              prompt="what are the app envvars?")
@click.option('--image', '-i', help='nebula app docker image', prompt="what is the app docker image?")
@click.option('--running', '-r', default=True, help='nebula app running/stopped state, defaults to True',
              prompt="should the app start in the running state?")
@click.option('--network_mode', '-n', default="bridge", prompt="what is the app network_mode?",
              help='nebula app network mode (host, bridge, etc...), defaults to bridge')
def create(app, starting_ports, containers_per, env_vars, image, running, network_mode):
    config_json = {"starting_ports": list(starting_ports), "containers_per": dict(containers_per),
                   "env_vars": dict(env_vars), "image": image, "running": running, "network_mode": network_mode}
    connection = NebulaCall()
    connection.create_app(app, config_json)


@nebulactl.command(help="delete a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to delete?', help='nebula app name to delete')
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


# todo - add the config variables needed
@nebulactl.command(help="update a nebula app")
@click.option('--app', '-a', prompt='what is nebula app name to update?', help='nebula app name to update')
def update(app):
    connection = NebulaCall()
    connection.update_app(app)


@nebulactl.command(help="rolling restart a nebula apps")
@click.option('--app', '-a', prompt='what is nebula app name to rolling restart?',
              help='nebula app name to rolling restart')
def roll(app):
    connection = NebulaCall()
    connection.roll_app(app)


if __name__ == '__main__':
    nebulactl()
