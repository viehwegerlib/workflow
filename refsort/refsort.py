'''refsort

Read a Markdown file via standard input and tidy its reference links. 
The reference links will be numbered in the order they appear in the text 
and placed at the bottom of the file.

Usage: refsort.py -i <infile> -o <outfile>

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -i --infile   /path/to/infile
  -o --outfile  /path/to/outfile

'''

# Adopted from:
# http://www.leancrew.com/all-this/2012/09/tidying-markdown-reference-links/

import sys
import re
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='refsort 0.1')
    # print(arguments)

# The regex for finding reference links in the text. Don't find
# footnotes by mistake.
link = re.compile(r'\[([^\]]+)\]\[([^^\]]+)\]')

# The regex for finding the label. Again, don't find footnotes
# by mistake.
label = re.compile(r'^\[([^^\]]+)\]:\s+(.+)$', re.MULTILINE)

def refrepl(m):
  'Rewrite reference links with the reordered link numbers.'
  return '[%s][%d]' % (m.group(1), order.index(m.group(2)) + 1)

# Read in the file and find all the links and references.
with open(arguments['<infile>']) as infile:
    text = infile.read()

links = link.findall(text)
labels = dict(label.findall(text))

# Determine the order of the links in the text. If a link is used
# more than once, its order is its first position.
order = []
for i in links:
  if order.count(i[1]) == 0:
    order.append(i[1])

# Make a list of the references in order of appearance.
newlabels = [ '[%d]: %s' % (i + 1, labels[j]) for (i, j) in enumerate(order) ]

# Remove the old references and put the new ones at the end of the text.
text = label.sub('', text).rstrip() + '\n'*3 + '\n'.join(newlabels)

# Rewrite the links with the new reference numbers.
text = link.sub(refrepl, text)

with open(arguments['<outfile>'], 'w+') as outfile:
    outfile.write(text)

