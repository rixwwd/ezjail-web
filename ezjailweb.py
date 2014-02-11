#!/usr/bin/env python
# coding: utf-8

import cherrypy
import ezjailwrapper
from jinja2 import Environment, FileSystemLoader
import os.path
import re

env = Environment(loader=FileSystemLoader('templates'))
current_dir = os.path.dirname(os.path.abspath(__file__))



def cmdexec(func):
  def wrapper(*args, **kwargs):
    try:
      func(*args, **kwargs)
    except ezjailwrapper.CommandExecuteException as ex:
      cherrypy.session['error_message'] = ex.error_msg
      raise cherrypy.HTTPRedirect("index")

  return wrapper



class EzjailWeb:
  
  @cherrypy.expose
  def index(self):
    jails = ezjailwrapper.list()
    tmpl = env.get_template('index.html')
    error_message = cherrypy.session.pop('error_message', None)
    return tmpl.render(jails=jails, error_message=error_message)


  @cherrypy.expose
  def new(self):
    tmpl = env.get_template('new.html')
    return tmpl.render()

  @cherrypy.expose
  @cmdexec
  def create(self, ipaddress, hostname):

    errors = {}
    if re.match("^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$", ipaddress) == None:
      errors['ipaddress'] = 'Invalid IP Address'

    if re.match("^[0-9a-zA-Z-\\._]+$", hostname) == None:
      errors['hostname'] = 'Invalid Hostname'

    if len(errors) > 0:
      tmpl = env.get_template('new.html')
      return tmpl.render(errors=errors, hostname=hostname, ipaddress=ipaddress)

    ezjailwrapper.create(hostname, ipaddress)

    raise cherrypy.HTTPRedirect("index")


  @cherrypy.expose
  @cmdexec
  def start(self, jailname):
    ezjailwrapper.start(jailname)
    raise cherrypy.HTTPRedirect("index")


  @cherrypy.expose
  @cmdexec
  def stop(self, jailname):
    ezjailwrapper.stop(jailname)
    raise cherrypy.HTTPRedirect("index")


cherrypy.quickstart(EzjailWeb(), config="ezjailweb.conf")

