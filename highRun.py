from google.appengine.ext import ndb

class HighRun(ndb.Model):
  handicap = ndb.IntegerProperty()
  target = ndb.IntegerProperty()

def insertJavascript(response):
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
