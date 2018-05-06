import argparse
from cumd.cumd import cumd


HTML_TEMPLATE = '''\
<html>
<head>
    <link rel="stylesheet" href="https://sci.ponomar.net/css/fonts.css" />
    <style>
        :root {
            --kinovar: rgb(204,8,3);
        }
        body {
            font-family: 'Ponomar Unicode'
        }
        wide {
            font-size: 130%%;
            display: inline-block;
            transform: scaleY(0.77);
        }
        red {
            display: inline;
            color: var(--kinovar);
        }
    </style>
</head>
<body>
%s
</body>
'''

parser = argparse.ArgumentParser(description='Converts CU markdown to HTML')
parser.add_argument('input', help='File name of the input *.md file')
parser.add_argument('output', help='File name of the output *.html file')
parser.add_argument('--html', action='store_true', default=False, help='Set to generate viewable HTML')

args = parser.parse_args()

with open(args.input, 'r', encoding='utf-8') as f:
    text = f.read()

body = cumd(text)
with open(args.output, 'w', encoding='utf-8') as f:
    if args.html:
        f.write(HTML_TEMPLATE % body)
    else:
        f.write(body)
