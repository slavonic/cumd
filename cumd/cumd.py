"""
Markdown extensions to support Church Slavonic
"""
import re
import markdown
import logging
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree as et
from . import __version__


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

RE_COMBINERS = ''.join(x for x in CU_COMBINERS + [CU_BREATHING, CU_BREATHING_HARD])
RE_DIGRAPHS = 'оу|Оу|ᲂу'

RE_CU_LETTER = '(?:' + RE_DIGRAPHS + '|\\w)[' + RE_COMBINERS + ']*'


class RedBukvaExtension(Extension):
    """Church Slavonic extensions to Markdown"""

    def extendMarkdown(self, md):
        """ Register extension instances. """
        md.inlinePatterns.register(RedBukvaPattern(), 'redBukva', 105)
        md.inlinePatterns.register(BukvitsaPattern(), 'bukvitsa', 105)
        md.inlinePatterns.register(KinovarPattern(), 'kinovar', 107)
        md.inlinePatterns.register(WidePattern(), 'wide', 107)
        md.inlinePatterns.register(PageBreakPattern(), 'pageBreak', 106)
        md.inlinePatterns.register(VerseLabelPattern(), 'verseLabel', 106)
        md.treeprocessors.register(BlockAttributeProcessor(), 'blockAttr', 100)

class RedBukvaPattern(InlineProcessor):
    """wraps first letter in <red> tag"""
    def __init__(self):
        InlineProcessor.__init__(self, r'~(' + RE_CU_LETTER + ')')

    def handleMatch(self, m, data):
        el = et.Element('red')
        el.text = m.group(1)
        return el, m.start(0), m.end(0)

class KinovarPattern(InlineProcessor):
    """wraps span in kinovar =xx="""
    def __init__(self):
        InlineProcessor.__init__(self, r'\=(\S|\S.*?\S)\=')

    def handleMatch(self, m, data):
        el = et.Element('red')
        el.text = m.group(1)
        return el, m.start(0), m.end(0)

class WidePattern(InlineProcessor):
    """wraps span in kinovar =xx="""
    def __init__(self):
        InlineProcessor.__init__(self, r'\+(\S|\S.*?\S)\+')

    def handleMatch(self, m, data):
        el = et.Element('wide')
        el.text = m.group(1)
        return el, m.start(0), m.end(0)

class BukvitsaPattern(InlineProcessor):
    """wraps first letter in <bukvitsa> tag"""
    def __init__(self):
        InlineProcessor.__init__(self, r'\^(' + RE_CU_LETTER + ')')

    def handleMatch(self, m, data):
        el = et.Element('bukvitsa')
        el.text = m.group(1)
        return el, m.start(0), m.end(0)

class PageBreakPattern(InlineProcessor):
    """handles page break anchors"""
    def __init__(self):
        InlineProcessor.__init__(self, r'<<(\d+)(?::\s*([^>)]+))?>>')

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
        InlineProcessor.__init__(self, r'\({2}\s*(.+?)\s*\){2}')

    def handleMatch(self, m, data):
        el = et.Element('verse')
        el.attrib['label'] = m.group(1)
        return el, m.start(0), m.end(0)

class BlockAttributeProcessor(Treeprocessor):
    def run(self, root):
        for block in root:
            if block.text is not None:
                block.text = self._doblock(block, block.text)

    def _doblock(self, block, text):
        def sub(mtc):
            expressions = mtc.group(1).split(',')
            for e in expressions:
                parts = e.split('=')
                if len(parts) != 2:
                    logging.warning('Could not parse expression %r' % e)
                else:
                    block.attrib[parts[0]] = parts[1]
            return ''
        return re.sub(r'\n?{{(.*?)}}\n?', sub, text)

class CuMarkdown(markdown.Markdown):
    """Church Slavonic version of Mardown class"""
    def __init__(self, *extensions):
        markdown.Markdown.__init__(
            self,
            extensions=[RedBukvaExtension(), *extensions],
            output_format='html5'
        )

def cumd(text, extensions=None):
    """converts markdown to html"""
    if extensions is None:
        extensions = []
    return CuMarkdown(*extensions).convert(text)


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
            letter-spacing: 0.1rem;
        }
        red {
            display: inline;
            color: var(--kinovar);
        }
        p[text_align="center"] {
            text-align: center;
        }
        bukvitsa {
            display: inline-block;
            height: 3rem;
            padding-right: 0.25rem;
            font-family: 'Indiction Unicode';
            font-size: 300%%;
            float: left;
            color: var(--kinovar);
            margin-top: -0.4rem;
        }
    </style>
</head>
<body>
%s
</body>
</html>
'''

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Converts CU markdown to HTML (version %s)' % __version__)
    parser.add_argument('input', help='File name of the input *.md file')
    parser.add_argument('output', help='File name of the output *.html file')
    parser.add_argument('--html', action='store_true', default=False, help='Set to generate viewable HTML')
    parser.add_argument('--extensions', '-e', help='List of comma-separated extensions to enable. For example -e footnotes,math')

    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()

    extensions = []
    if args.extensions:
        extensions = args.extensions.split(',')
    body = cumd(text, extensions=extensions)
    with open(args.output, 'w', encoding='utf-8') as f:
        if args.html:
            f.write(HTML_TEMPLATE % body)
        else:
            f.write(body)

if __name__ == '__main__':
    #print(repr(RE_CU_LETTER))
    main()
