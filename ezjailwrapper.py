# coding: utf-8

import subprocess

# EZJAIL_CMD="/usr/local/bin/ezjail-admin"
EZJAIL_CMD=["/usr/bin/ssh"]
EZJAIL_OPT="root@jailhost ezjail-admin".split()

class CommandExecuteException(Exception):
  def __init__(self, error_msg):
    self.error_msg = error_msg


def create(jailname, ipaddress):
  return execute(['create', jailname, ipaddress])


def delete(jailname):
  return execute(['delete', '-wf', jailname])

  
def list():
  output = execute(['list'])
  lines = output.splitlines()
  
  key = ('status','jid','ip','hostname','directory')
  
  if len(lines) >= 3:
    jail_list = [l.split() for l in lines[2:]]
    return [dict(zip(key, jail)) for jail in jail_list]
  else:
    return []


def start(jailname):
  return execute(['onestart', jailname])


def stop(jailname):
  return execute(['onestop', jailname])


def execute(cmd):
  try:
    output = subprocess.check_output(EZJAIL_CMD + EZJAIL_OPT + cmd, stderr=subprocess.STDOUT).decode('utf-8')
  except subprocess.CalledProcessError as ex:
    raise CommandExecuteException(ex.output.decode('utf-8'))
  return output
