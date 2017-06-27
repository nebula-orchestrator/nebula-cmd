#!/usr/bin/env python
import click, json
from NebulaPythonSDK import Nebula
from os.path import expanduser


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
        print self.connection.create_app(app, config).text

    def delete_app(self, app):
        print self.connection.delete_app(app).text

    def list_apps(self):
        reply = self.connection.list_apps().json()
        if len(reply["apps"]) == 0:
            print "no apps in nebula cluster"
        else:
            print "nebula cluster apps:"
            for app in reply["apps"]:
                print app

    def list_app_info(self, app):
        print self.connection.list_app_info(app).text

    def stop_app(self, app):
        print self.connection.stop_app(app).text

    def start_app(self, app):
        print self.connection.start_app(app).text
        
    def restart_app(self, app):
        print self.connection.restart_app(app).text

    def update_app(self, app, config):
        print self.connection.update_app(app, config).text

    def roll_app(self, app):
        print self.connection.roll_app(app).text


@click.group(help="manage a nebula cluster")
def nebulactl():
    pass


@nebulactl.command(help="login to nebula")
@click.option('--username', prompt='what is nebula api-manager basic auth username?', help='nebula api-manager basic '
                                                                                           'auth username')
@click.option('--password', prompt='what is nebula api-manager basic auth password?', help='nebula api-manager basic '
                                                                                           'auth password')
@click.option('--host', prompt='what is nebula api-manager host?', help='nebula api-manager host.')
@click.option('--port', prompt='what is nebula api-manager port?', help='nebula api-manager port', default=80)
@click.option('--protocol', prompt='what is nebula api-manager protocol?', help='nebula api-manager protocol',
              default="http")
def login(username, password, host, port, protocol):
    home = expanduser("~")
    auth_file = open(home + "/.nebula.json", "w+")
    json.dump({"username": username, "password": password, "host": host, "port": port, "protocol": protocol}, auth_file)


@nebulactl.command(help="list nebula apps")
def list():
    connection = NebulaCall()
    connection.list_apps()


@nebulactl.command(help="create a new nebula app")
@click.option('--app', prompt='what is nebula app name to create?', help='nebula app name to create')
def create(app):
    connection = NebulaCall()
    connection.create_app(app)


@nebulactl.command(help="delete a nebula app")
@click.option('--app', prompt='what is nebula app name to delete?', help='nebula app name to delete')
def delete(app):
    connection = NebulaCall()
    connection.delete_app(app)


@nebulactl.command(help="list info of a nebula app")
@click.option('--app', prompt='what is nebula app name to get info of?', help='nebula app name to get info of')
def info(app):
    connection = NebulaCall()
    connection.list_app_info(app)


@nebulactl.command(help="start a nebula app")
@click.option('--app', prompt='what is nebula app name to start?', help='nebula app name to start')
def start(app):
    connection = NebulaCall()
    connection.start_app(app)


@nebulactl.command(help="stop a nebula app")
@click.option('--app', prompt='what is nebula app name to stop?', help='nebula app name to stop')
def stop(app):
    connection = NebulaCall()
    connection.stop_app(app)


@nebulactl.command(help="restart a nebula app")
@click.option('--app', prompt='what is nebula app name to restart?', help='nebula app name to restart')
def restart(app):
    connection = NebulaCall()
    connection.restart_app(app)


@nebulactl.command(help="update a nebula app")
@click.option('--app', prompt='what is nebula app name to update?', help='nebula app name to update')
def update(app):
    connection = NebulaCall()
    connection.update_app(app)


@nebulactl.command(help="rolling restart a nebula apps")
@click.option('--app', prompt='what is nebula app name to rolling restart?', help='nebula app name to rolling restart')
def roll(app):
    connection = NebulaCall()
    connection.roll_app(app)


if __name__ == '__main__':
    nebulactl()
