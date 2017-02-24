files = ('cpython27', 'cython', 'pypy', 'pyston')
res = {}

for file in files:
    for line in open(file, 'r'):
        v,n,t = line.strip().split(',')
        res.setdefault(file,{})
        res[file][' '.join((v,n))] = t

labels = sorted(res[file].keys())
label_headers = ''.join([' <td>{}</td>\n'.format(label) for label in labels])

top = '''<html>
<body>
<p>Lower is better</p>
<table>
<tr>
 <th>Interpreter</th>
{}
</tr> 
'''.format(label_headers)


for file in files:
    top += '\n<tr>\n<td>{}</td>'.format(file)
    for label in labels:
        top += '\n<td>{}</td>'.format(res[file][label])
    top += '\n</tr>\n'

top += '</table></body></html>'
print top
