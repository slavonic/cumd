"""
Markdown extensions to support Church Slavonic
"""
import re
import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.util import etree as et


CU_ACCENTS_1 = [  # Aleksandr put only those for the start of the word patterns
    '\u0300',
    '\u0301',
    '\u0311',
    '\u0308'
]

CU_ACCENTS_2 = [
    chr(x) for x in range(ord('\u2de0'), ord('\u2dff')+1)
] + [
    chr(x) for x in range(ord('\ua674'), ord('\ua67d')+1)
]

CU_COMBINERS = CU_ACCENTS_1 + [
    '\u0486',
    '\u0306',
    '\u033e',
    '\ua67d',
    '\ua67c',
    '\u0307',
    '\u030f',
    '\u0483',
    '\u0487',
] + CU_ACCENTS_2

CU_BREATHING = '\u0486'
CU_BREATHING_HARD = '\u0485'

RE_COMBINERS = ''.join(re.escape(x) for x in CU_COMBINERS + [CU_BREATHING, CU_BREATHING_HARD])
RE_DIGRAPHS = 'оу|Оу|ᲂу'

RE_CU_LETTER = '(?:' + RE_DIGRAPHS + '|\\S)[' + RE_COMBINERS + ']*'


class RedBukvaExtension(Extension):
    """Church Slavonic extensions to Markdown"""

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['redBukva'] = RedBukvaPattern()
        md.inlinePatterns['emphasis'].tag = 'red'
        md.inlinePatterns['strong'].tag = 'wide'
        md.inlinePatterns['pageBreak'] = PageBreakPattern()
        md.inlinePatterns['verseLabel'] = VerseLabelPattern()

class RedBukvaPattern(InlineProcessor):
    """wraps first letter in <red> tag"""
    def __init__(self):
        InlineProcessor.__init__(self, r'~(' + RE_CU_LETTER + ')')

    def handleMatch(self, m, data):
        el = et.Element('red')
        el.text = m.group(1)
        return el, m.start(0), m.end(0)

class PageBreakPattern(InlineProcessor):
    """handles page break anchors"""
    def __init__(self):
        InlineProcessor.__init__(self, r'<<(\d+)(:[^>)]+)?>>')

    def handleMatch(self, m, data):
        el = et.Element('anchor')
        number = m.group(1)
        label = m.group(2)
        if not label:
            label = number
        el.attrib['page'] = number
        el.attrib['label'] = label
        return el, m.start(0), m.end(0)

class VerseLabelPattern(InlineProcessor):
    """handles verse numbering anchors"""
    def __init__(self):
        InlineProcessor.__init__(self, r'\({2}(.+?)\){2}')

    def handleMatch(self, m, data):
        el = et.Element('verse')
        el.attrib['label'] = m.group(1)
        return el, m.start(0), m.end(0)

class CuMarkdown(markdown.Markdown):
    """Church Slavonic version of Mardown class"""
    def __init__(self):
        markdown.Markdown.__init__(
            self,
            extensions=[RedBukvaExtension()],
            output_format='html5'
        )

def cumd(text):
    """converts markdown to html"""
    return CuMarkdown().convert(text)


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

def main():
    import argparse
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

if __name__ == '__main__':
    main()
