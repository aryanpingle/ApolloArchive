import re

s = "hello <br> hheefe<br><br>"
s = re.sub(r'(<br>)+$', '', s)

print(s)