class AddPerson():
  def show(self, response):
    response.write('<hr/><form action="." method="post">\n')
    response.write('  <table>\n')
    response.write('    <tr><td rowspan=2>New Player\n')
    response.write('      <td>First: <input name="firstName" value="" size="20"/>\n')
    response.write('      <td class="right">Handicap: <input onchange=\'highRun("handicap","highRunTarget")\' id="handicap" name="handicap" value="" size="5"/>\n')
    response.write('      <td rowspan=2><input type="Button" value="Add New Player"/>\n')
    response.write('    <tr><td>Last: <input name="lastName" value="" size="20"/>\n')
    response.write('      <td class="right">High Run Target: <input id="highRunTarget" name="highRunTarget" value="" size="5"/>\n')
    response.write('  </table>\n')
    response.write('</form>\n')
