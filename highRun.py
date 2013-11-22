from google.appengine.ext import ndb

class HighRun(ndb.Model):
  handicap = ndb.IntegerProperty()
  target = ndb.IntegerProperty()
  
  def destroy(self):
    # Delete all old data
    ndb.delete_multi(HighRun.query().fetch(keys_only=True))

  def create(self):
    # Create all the handicaps
    if HighRun.query().get() is None:
      self.createEntry(400, 18)
      self.createEntry(450, 20)
      self.createEntry(500, 22)
      self.createEntry(550, 26)
      self.createEntry(600, 32)
      self.createEntry(650, 44)
      self.createEntry(700, 58)
      self.createEntry(725, 72)
      self.createEntry(750, 86)
      self.createEntry(775, 100)
      self.createEntry(800, 114)
      self.createEntry(825, 128)
      self.createEntry(850, 144)

  def createEntry(self, hcap, tgt):
    hrun = HighRun()
    hrun.handicap = hcap
    hrun.target = tgt
    hrun.put()

def insert(response):
  response.write('  function highRun(handicapName, highrunName) {\n')
  response.write('    var handicapElement = document.getElementById(handicapName);\n')
  response.write('    var highrunElement = document.getElementById(highrunName);\n')
  response.write('    var hcap = handicapElement.value;\n')
  response.write('    var tgt = 0;\n')
  
  response.write('    if (hcap >= 100 && hcap < 1000) {\n')
  prevHcap = 0
  prevTgt = 0
  prefix = ''
  for run in HighRun.query().order(HighRun.handicap):
    scale = float(run.handicap - prevHcap) / (run.target - prevTgt)
    response.write('      {0}if(hcap < {1}) tgt = {2} + (hcap - {3}) / {4};\n'.
        format(prefix, run.handicap, prevTgt, prevHcap, scale))
    prevHcap = run.handicap
    prevTgt = run.target
    prefix = 'else '
    
  response.write('      else tgt = {0} + (hcap - {1}) / {2:.4f};\n'.
      format(prevTgt, prevHcap, scale))
  response.write('      highrunElement.value = tgt.toFixed(2);\n')
  response.write('    } else {\n')
  response.write('      highrunElement.value = "";\n')
  response.write('    }\n')
  response.write('  }\n')
