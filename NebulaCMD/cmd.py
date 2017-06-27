from NebulaPythonSDK import Nebula


class NebulaCMD:

    def __init__(self,):
        try:
            auth_file = open("~/.nebula/nebula.json", "r")
            auth_json = dict(auth_file.read())
            self.connection = Nebula(username=auth_json["username"], password=auth_json["password"],
                                     host=auth_json["host"], port=auth_json["port"], protocol=auth_json["protocol"])
        except:
            print "error reading ~/.nebula/nebula.json auth file, try logging in first"
            exit(2)

    def create_app(self, app, config):
        print self.connection.create_app(app, config)

    def delete_app(self, app):
        print self.connection.delete_app(app)

    def list_apps(self):
        print self.connection.list_apps()

    def list_app_info(self, app):
        print self.connection.list_app_info(app)

    def stop_app(self, app):
        print self.connection.stop_app(app)

    def start_app(self, app):
        print self.connection.start_app(app)
        
    def restart_app(self, app):
        print self.connection.restart_app(app)

    def update_app(self, app, config):
        print self.connection.update_app(app, config)

    def roll_app(self, app):
        print self.connection.roll_app(app)

    def login(self):
        auth_file = open("~/.nebula/nebula.json", "w")
        user = raw_input("please enter nebula username: ")
        password = raw_input("please enter nebula password: ")
        host = raw_input("please enter nebula host (for example: nebula.example.com): ")
        port = raw_input("please enter nebula port: ")
        protocol = raw_input("please enter nebula protocol (http or https): ")
        auth_file.write(str({"user": user, "password": password, "host": host, "port": port, "protocol": protocol}))
        auth_json = dict(auth_file.read())
        self.connection = Nebula(username=auth_json["username"], password=auth_json["password"], host=auth_json["host"],
                                 port=auth_json["port"], protocol=auth_json["protocol"])
