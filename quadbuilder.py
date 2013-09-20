import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from models import *
from AddHandlers import *
from data_validation import *
import hashes

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'])

###############################################################
# Abstract Handler - for jinja template usage #################
###############################################################
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = JINJA_ENVIRONMENT.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
###############################################################
# MainPage handler ############################################
###############################################################
class MainPage(Handler):

    def get(self):
        # Authenticate
        user_id = Authenticate(self.request)
        user = None
        if user_id:
            user = User.get_by_id(int(user_id))

        ######### Getting Specs from DB ###########
        specs = Spec.query().fetch(6)

        self.render("newIndex.html", user=user,
                                  specs=specs,)
###############################################################
# AllBuildsHandler ############################################
###############################################################
class AllBuildsHandler(Handler):

    def get(self):
        # Authenticate
        user_id = Authenticate(self.request)
        user = None
        if user_id:
            user = User.get_by_id(int(user_id))

        ######### Getting Specs from DB ###########
        specs = Spec.query().fetch()

        # This is a call to newIndex, but this time using ALL builds
        self.render("newIndex.html", user=user,
                                  specs=specs,)
###############################################################
# NewBuildHandler #############################################
###############################################################
class NewBuildHandler(Handler):

    def get(self):
        # Authenticate
        user_id = Authenticate(self.request)
        user = None
        if user_id:
            user = User.get_by_id(int(user_id))
        ######### Getting Parts from DB ###########
        motors = Motor.query().fetch()
        escs = Esc.query().fetch()
        props = Prop.query().fetch()

        self.render("newNewBuild.html", user=user,
                                  motors=motors,
                                  escs=escs,
                                  props=props,)
###############################################################
# AddHandler - main page for adding parts. ####################
###############################################################
class AddHandler(Handler):

    def get(self):
        # Authenticate
        user_id = Authenticate(self.request)
        user = None
        if user_id:
            user = User.get_by_id(int(user_id))

        self.render("newAdd.html", user=user)
###############################################################
# PermalinkHandler ############################################
###############################################################
class PermalinkHandler(Handler):

    def get(self, kind, entry_id):
        # Authenticate
        user_id = Authenticate(self.request)
        user = None
        if user_id:
            user = User.get_by_id(int(user_id))

        # Find Category and object from DB.    
        obj = None
        if kind == 'Motor':
            obj = Motor.get_by_id(int(entry_id))
        elif kind == 'ESC':
            obj = Esc.get_by_id(int(entry_id))
        elif kind == 'Prop':
            obj = Prop.get_by_id(int(entry_id))
        elif kind == 'Spec':
            obj = Spec.get_by_id(int(entry_id))
        elif kind == 'User':
            obj = User.get_by_id(int(entry_id))
            ######### Getting Specs from DB ###########
            specs = obj.specsKey
            # for spec in specs:
                # self.response.write(spec.get().toString())
            specs = [spec.get() for spec in specs]
            self.render("newUserPage.html", user=user,
                                            obj=obj,
                                            specs=specs,)

        if obj:
            self.response.write(obj.toString())
        else:
            self.response.write("No such part.")        
###############################################################
# User handlers ###############################################
###############################################################
def Authenticate(request):
        h = request.cookies.get('name')
        user_id = hashes.check_secure_val(h)
        return user_id

class LoginHandler(Handler):

    def get(self):
        self.render("newLogin.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        user = User.query().filter(User.name==username).fetch(1)
        if user:
            user = user[0]
            pw_hash = user.pw_hash
            if username and password and hashes.valid_pw(username, password, pw_hash):
                user_id = str(user.key.id())
                secure_val = hashes.make_secure_val(user_id)
                self.response.headers.add_header('Set-Cookie', str('name=%s; Path=/' % secure_val))
                self.redirect("/")
            else:
                self.render("newLogin.html",error="Invalid username or password." )
        else:
            self.render("newLogin.html",error="Invalid username or password.")
        
class SignupHandler(Handler):

    def get(self):
        self.render("newSignup.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify   = self.request.get("verify")
        email    = self.request.get("email")

        username_error=""
        password_error=""
        verify_error=""
        email_error=""

        if not valid_username(username):
            username_error = "Invalid username."
        if not valid_password(password):
            password_error = "Invalid password."
        if valid_password(password) and (password != verify):
            verify_error = "Password not verified."
        if not valid_email(email):
            email_error = "Invalid email address."

        # Check for duplicate user-names:
        user = User.query().filter(User.name==username).fetch(1)
        if user:
            user = user[0]
            username_error = "User %s already exists." % user.name
            self.render("newSignup.html", username=username,
                                       email=email,
                                       username_error=username_error)
        else:
            if (valid_username(username) and
                valid_password(password) and (password == verify) and
                valid_email(email)):
                pw_hash = hashes.make_pw_hash(username, password)
                u = User(name=username,pw_hash=pw_hash)
                u_key = u.put()
                user_id = str(u_key.id())
                secure_val = hashes.make_secure_val(user_id)
                self.response.headers.add_header('Set-Cookie', str("name=%s; Path=/" % secure_val))
                self.redirect("/")
            else:
                self.render("newSignup.html", username=username,
                                           email=email,
                                           username_error=username_error,
                                           password_error=password_error,
                                           verify_error=verify_error,
                                           email_error=email_error)

class LogoutHandler(Handler):

    def get(self):
        h = self.request.cookies.get('name')
        user_id = hashes.check_secure_val(h)
        if user_id:
            self.response.headers.add_header("Set-Cookie", "name=; Path=/")
        self.redirect("/")
###############################################################

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/AllBuilds', AllBuildsHandler),
    ('/NewBuild', NewBuildHandler),
    ('/Add', AddHandler),
    ('/AddMotor', AddMotor),
    ('/AddEsc', AddEsc),
    ('/AddProp', AddProp),
    ('/AddSpec', AddSpec),
    ('/(Motor|ESC|Prop|Spec|User)/(\d+)', PermalinkHandler),
    ('/Login', LoginHandler),
    ('/Signup', SignupHandler),
    ('/Logout', LogoutHandler),
], debug=True)