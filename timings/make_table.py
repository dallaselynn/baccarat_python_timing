files = ('cpython27', 'cython', 'pypy', 'pyston')
res = {}

for file in files:
    for line in open(file, 'r'):
        v,n,t = line.strip().split(',')
        res.setdefault(file,{})
        res[file][' '.join((v,n))] = t

labels = sorted(res[file].keys())
label_headers = ''.join([' <td>{}</td>\n'.format(label) for label in labels])

def make_table():
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


def make_graph():
  v1_nums = dict(cpython27={}, cython={}, pypy={}, pyston={})
  v2_nums = dict(cpython27={}, cython={}, pypy={}, pyston={})
  v3_nums = dict(cpython27={}, cython={}, pypy={}, pyston={})

  for n in res.keys():
    #print 'processing %s' % n
    for label,num in res[n].items():
      key,iters = label.split()
      if key == 'v1':
        v1_nums[n][iters] = num
      elif key == 'v2':
        v2_nums[n][iters] = num
      elif key == 'v3':
        v3_nums[n][iters] = num
      else:
        raise 'Unknown key %s' % key

  make_png('v1', v1_nums)
  make_png('v2', v2_nums)
  make_png('v3', v3_nums)


def make_png(name, data):
  import matplotlib.pyplot as plt
  import numpy as np

  N = 6 
  width = 0.20
  ind = np.arange(N)

  fig, ax = plt.subplots()

  cpython_nums = [data['cpython27'][x] for x in sorted(data['cpython27'])]
  pypy_nums = [data['pypy'][x] for x in sorted(data['pypy'])]
  pyston_nums = [data['pyston'][x] for x in sorted(data['pyston'])]
  cython_nums = [data['cython'][x] for x in sorted(data['cython'])]

  rects1 = ax.bar(ind, cpython_nums, width, color='r')
  rects2 = ax.bar(ind + width, pypy_nums, width, color='y')
  rects3 = ax.bar(ind + (width*2), pyston_nums, width, color='g')
  rects4 = ax.bar(ind + (width*3), cython_nums, width, color='b')

  ax.set_xlabel('Hands Played')
  ax.set_ylabel('Time (seconds)')
  ax.set_title('Time to Play x Hands %s (lower is better)' % name)
  iterations = ['10','100','1000','10000','100000','1000000']
  ax.set_xticks(ind + width * 2)
  ax.set_xticklabels(iterations)

  ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]),
            ('CPython', 'PyPy', 'Pyston', 'Cython'), loc=2)

  plt.savefig(name + '.png')


if __name__ == '__main__':
  make_graph()
