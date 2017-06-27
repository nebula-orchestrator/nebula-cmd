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


@click.group()
def nebulactl():
    pass


@nebulactl.command(help="login to nebula")
@click.option('--username', prompt='nebula api-manager basic auth username', help='The person to greet.')
@click.option('--password', prompt='nebula api-manager basic auth password', help='The person to greet.')
@click.option('--host', prompt='nebula api-manager host', help='The person to greet.')
@click.option('--port', prompt='nebula api-manager port', help='The person to greet.', default=80)
@click.option('--protocol', prompt='nebula api-manager protocol', help='The person to greet.', default="http")
def login(username, password, host, port, protocol):
    home = expanduser("~")
    auth_file = open(home + "/.nebula.json", "w+")
    json.dump({"username": username, "password": password, "host": host, "port": port, "protocol": protocol}, auth_file)


@nebulactl.command(help="list nebula apps")
def list():
    connection = NebulaCall()
    connection.list_apps()

if __name__ == '__main__':
    nebulactl()
