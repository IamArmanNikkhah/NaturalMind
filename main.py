import sys
sys.setrecursionlimit(2**30)


import numpy as np
import threading
from random import randrange
import random
import math
import time


class presynaps:
  
  def __init__(self):
    self.epsilonchange = 0.5
    self.data = random.uniform(-5,5)
  def strengthen(self):
    self.data += self.epsilonchange
  def weaken(self):
    self.data -= self.epsilonchange
  def setdata(self,d):
    self.data = d
  def sendtransmiter(self):
    return self.data

class postsynaps:
  
  def __init__(self,dendrite):
    self.epsilonchange = 0.05
    self.used = False
    self.mydendrite = dendrite
    self.receptor = random.uniform(0,1)
 
  def occupy(self):
    self.used = True
  def free(self):
    self.used = False
  def strengthen(self):
    self.receptor += self.epsilonchange
  def weaken(self):
    self.receptor = max(0,self.receptor-self.epsilonchange)
  def setfraction(self,f):
    self.receptor = f
  def gettransmiter(self,d):
    self.mydendrite.getsignal(self.receptor * d)

class synapse:
 
  def __init__(self,pre,post):
    self.presynaps = pre
    self.postsynapse = post
    self.postsynapse.occupy()
    self.calf = 0
  
  def transfertransmiter(self):
    self.calf = self.presynaps.sendtransmiter()
    #self.postsynapse.gettransmiter(self.calf)
    #self.calf = 0

  def setpresynaps(self,t):
    self.presynaps.setdata(t)

  def setpostsynaps(self,t):
    self.postsynapse.setfraction(t)

class axon:
  # Postsynaps should be like this : [p1,p2,.....]
  def __init__(self,Nuron):
    self.Nuron = Nuron
    self.presynapses = []
    self.terminal = []
  
  def addterminal(self,onePost):
    pre = presynaps()
    self.presynapses.append(pre)
    self.terminal.append(synapse(pre,onePost))
  
  def setterminal(self,w):
    if len(w)== len(self.presynapses):
      for i in range(0,len(self.presynapses)):
        self.presynapses[i].setdata(w[i])
    else:
      raise Exception('w should have size same size as presynapses. The value of w was: {}'.format(w))
  
  def freetransmiter(self,i):
    self.terminal[i].transfertransmiter()
  
  
  def sendsignal(self):
    processes = []
    for i in range (0,len(self.terminal)):
      p = threading.Thread(target=self.freetransmiter, args=(i,))
      p.start()
      processes.append(p)
    
    for process in processes:
      process.join()
  
    
  
class dendrite:
  
  def __init__(self,Nuron):
    self.Nuron = Nuron
    self.postsynapses = []
    self.inputSynapses = []

  def addInputSynapse(self,onePre):
    post = postsynaps(self)
    self.postsynapses.append(post)
    self.inputSynapses.append(synapse(onePre,post))
  
  def setreceptors(self,f):
    if len(f) == len(self.postsynapses):
      for i in range(0,len(self.postsynapses)):
        self.postsynapses.setfraction(f[i])
    else:
      raise Exception('f should have same size as postsynapses. The value of f was: {}'.format(w))
 
  def getsignal(self,data):
    self.Nuron.addvolt(data)

  def freetransmiter(self,i):
    self.terminal[i].transfertransmiter()
  
  
  def sendsignal(self):
    processes = []
    for i in range (0,len(self.terminal)):
      p = threading.Thread(target=self.freetransmiter, args=(i,))
      p.start()
      processes.append(p)
    
    for process in processes:
      process.join()



class MRI:
  def __init__(self):
    self.records = []

  def record(self,nuron):
    self.records.append(nuron)

  def result(self):
    print(self.records)


class Nuron:
 
  def __init__(self,name = "not defined",block, field):
    self.block = block
    self.brainField = field
    self.restVolt = -70
    self.thershold = -55
    self.maxvolt = 40
    self.name = name # name only used for mri
    self.volt = self.restVolt
    self.axon = axon(self)
    self.dendrite = dendrite(self)
    self.frequancy = 1
  
  def intialize_mri(self,mri):
    self.mri = mri
  
   def sendMassagetoBlock(self):
    msg = Massage(self,self.block,"spike")
    self.block.listentoSpike(msg)
  
  def refractory_period(self):
    absolute_refractory_voltage = -1000
    absolute_refractory_period = 1
    relative_refractory_voltage = -85
    relative_refractory_period = 3
    self.volt = absolute_refractory_voltage
    time.sleep(absolute_refractory_period/1000)
    self.volt = relative_refractory_voltage
    time.sleep(relative_refractory_period/1000)
    self.volt = self.restVolt
  
  
  def fire(self):
    self.mri.record(self.name)
    print(self.name) # TEST
    p1 = threading.Thread(target=self.axon.sendsignal, args=(,))
    p1.start()
    p2 = threading.Thread(target=self.refractory_period, args=(,))
    p2.start()
    p3 = threading.Thread(target=self.sendMassagetoBlock, args=(,))
    p3.start()
    p1.join()
    p2.join()
    p3.join()

    for i in range(1,self.frequancy):
      self.axon.sendsignal()
      time.sleep()
    
  
  #parameter 1
  def setfrequancy(self,freq):
    if freq >= 0 :
      self.frequancy = freq
  #parameter 2
  def setreceptors_dendrite(self,f):
    self.dendrite.setreceptors(f)
  
  #parameter 3
  def setterminal_axon(self,t):
    self.axon.setterminal(t)
  
  def returnpostsynapses(self):
    return self.dendrite.postsynapses

  def addvolt(self,v):
    self.volt = self.volt + v
    if self.volt >= self.thershold :
      self.volt = self.maxvolt
      self.fire()

class Massage:
  def __init__(self,sender, receiver, text):
    self.sender = sender
    self.receiver = receiver
    self.text = text  
  def readMsg(self):
    return self.text

class Location:
  def __init__(self,x,y):
    self.x = x
    self.y = y
  
  def distance(self,loc):
    dis = math.sqrt((self.x - loc.x)**2 + (self.y - loc.y)**2)  
    return dis

class Block:
  def __init__(self,loc,listener):
    self.blockVolt = 0
    self.location = loc
    self.voltageListener = listener
  
  def addVolt(self,volt):
    if volt > 0:
      self.blockVolt += volt

  def discharge(self):
    self.blockVolt = 0

  def sendMassagetoBrainField(self):
    msg = Massage(self,self.voltageListener,self.location)
    self.voltageListener.listentoVoltage(msg)

  def listentoSpike(self,msg):
    if msg.sender instanceof Nuron and msg.receiver instanceof Block:
      self.sendMassagetoBrainField()


class BrainField:
  def __init__(self,length,width,io = False):
    self.length = length #upper side is length
    self.width = width
    self.isIO = io
    self.blocks = [[Block(Location(i,j),self) for j in self.length] for i in self.width]
    self.baseField = 5
  
  def transferField(self,startBlock,endBlock):
    distance = startBlock.location.distance(endBlock.location)
    field = self.baseField / distance
    endBlock.addVolt(field)
  
  
  
  def listentoVoltage(self,msg):
    if self.isIO==False and msg.sender instanceof Block and msg.receiver instanceof BrainField:
      loc = msg.readMsg()
      spikedBlock = self.blocks[loc.x][loc.y]
      processes = []
      for i in range (max(0,loc.x - 2),min(self.width,(loc.x + 2) + 1)):
        for j in range (max(0,loc.y - 2),min(self.length,(loc.y + 2) + 1)):
          p = threading.Thread(target=self.transferField, args=(spikedBlock,self.blocks[i][j]))
          p.start()
          processes.append(p)
    
      for process in processes:
        process.join()

def connect2nuron(a,b):
  for i in range (0,len(b.dendrite.postsynapses)):
    if b.dendrite.postsynapses[i].used is not True:
      freePostSynaps = b.dendrite.postsynapses[i]
      break
  a.axon.addterminal(freePostSynaps)
  


if __name__ == '__main__':
  A = Nuron("A")
  B = Nuron("B")
  C = Nuron("C")
  D = Nuron("D")
  test = Nuron("test")
  mri = MRI()
  A.intialize_mri(mri)
  B.intialize_mri(mri)
  C.intialize_mri(mri)
  D.intialize_mri(mri)
  test.intialize_mri(mri)

  A.axon.setpostsynaps([B.dendrite.postsynapses[0],C.dendrite.postsynapses[0],D.dendrite.postsynapses[0]])
  B.axon.setpostsynaps([C.dendrite.postsynapses[1],D.dendrite.postsynapses[1]])
  C.axon.setpostsynaps([D.dendrite.postsynapses[2]])
  D.axon.setpostsynaps([])
  connect2nuron(D,test)

  A.setterminal_axon([15,15,15])
  B.setterminal_axon([15,15])
  C.setterminal_axon([15])
  D.setterminal_axon([15])

  A.fire()
  mri.result()
  print(D.volt)
