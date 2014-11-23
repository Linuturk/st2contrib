#!/usr/bin/python

import os, sys, re

class checkProcs(object):

  myPid = 0
  state = ""
  name = ""
  pid = 0
  allProcs = []
  interestingProcs = []
  procDir = "/proc"
  debug = False

  def __init__(self):
    self.myPid = os.getpid()

  def setup(self,debug=False):
    self.debug = debug
    if debug is True: print "Debug is on"
    self.allProcs = [procs for procs in os.listdir(self.procDir) if procs.isdigit() and int(procs) != int(self.myPid)]

  def process(self,criteria):
    for p in self.allProcs:
      fh = open(self.procDir + "/" + p + "/stat")
      pInfo = fh.readline().split()
      cmdfh = open(self.procDir + "/" + p + "/cmdline")
      cmd = cmdfh.readline()
      pInfo[1] = cmd
      if criteria == 'state':
        if pInfo[2] == self.state:
          self.interestingProcs.append(pInfo)
      elif criteria == 'name':
        if re.search(self.name,pInfo[1]):
            self.interestingProcs.append(pInfo)
      elif criteria == 'pid':
        if pInfo[0] == self.pid:
          self.interestingProcs.append(pInfo)
      fh.close()

  def byState(self, state):
    self.state = state
    self.process(criteria='state')
    self.show()

  def byPid(self, pid):
    self.pid = pid
    self.process(criteria='pid')
    self.show()

  def byName(self,name):
    self.name = name
    self.process(criteria='name')
    self.show()

  def run(self,foo,criteria):
    if foo == 'state':
      self.byState(criteria)
    elif foo == 'name':
      self.byName(criteria)
    elif foo == 'pid':
      self.byPid(criteria)

  def show(self):
    prettyOut = ""
    if len(self.interestingProcs)>0:
      for proc in self.interestingProcs:
        prettyOut += "%s %s - time:%s\n" % (proc[0],proc[1],proc[13])
    else:
      prettyOut = "No processes matched criteria"

    print prettyOut


if __name__ == '__main__':

  foo = checkProcs()
  foo.setup(debug=False)
  foo.run(sys.argv[1],sys.argv[2])
