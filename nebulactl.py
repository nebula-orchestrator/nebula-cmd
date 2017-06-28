#!/usr/bin/env python2.7
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
        # todo - print a real reply
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


# todo - add the config variables needed
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


# todo - add the config variables needed
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
