"""
converts from culiturgical XML to cu-Markdown
"""
import re
import lxml.etree as et
import lxmlx.event as ev
from cumd.cumd import RE_CU_LETTER


def _ns(name):
    return '{http://www.ponomar.net/culiturgical}' + name


def detect_first_letter(blob):
    """replaces <red>b</red>lah with <redletter>b</redletter>"""
    return re.sub(r'(<red>)(' + RE_CU_LETTER + ')(</red>)([^\s<])', '<redletter>\\2</redletter>\\4', blob)

def md(events):
    """converts XML markup to text (cu-flavored markdown)"""
    for obj, peer in ev.with_peer(events):
        if obj['type'] == ev.ENTER:
            if obj['tag'] == _ns('p'):
                yield dict(type=ev.TEXT, text='\n\n')
            elif obj['tag'] == _ns('small'):
                pass
            elif obj['tag'] == _ns('redletter'):
                yield dict(type=ev.TEXT, text='~')
            elif obj['tag'] == _ns('red'):
                yield dict(type=ev.TEXT, text='=')
            elif obj['tag'] == _ns('wide'):
                yield dict(type=ev.TEXT, text='+')
            elif obj['tag'] == _ns('footnote'):
                yield dict(type=ev.TEXT, text='[[')
            elif obj['tag'] == _ns('anchor'):
                number = obj['attrib']['number']
                label =  obj['attrib']['label']
                if number == label:
                    yield dict(type=ev.TEXT, text='<<%s>>' % number)
                else:
                    yield dict(type=ev.TEXT, text='<<%s: %s>>' % (label, number))
            elif obj['tag'] == _ns('verse'):
                label =  obj['attrib']['label']
                yield dict(type=ev.TEXT, text='((%s))' % label)
            elif obj['tag'] == _ns('disp'):
                pass
            elif obj['tag'] == _ns('img'):
                yield dict(type=ev.TEXT, text='[!image](%s)' % obj['attrib']['src'])
            else:
                assert False, obj

        elif obj['type'] == ev.EXIT:
            if peer['tag'] == _ns('p'):
                pass
            elif peer['tag'] == _ns('small'):
                pass
            elif peer['tag'] == _ns('redletter'):
                pass
            elif peer['tag'] == _ns('red'):
                yield dict(type=ev.TEXT, text='=')
            elif peer['tag'] == _ns('wide'):
                yield dict(type=ev.TEXT, text='+')
            elif peer['tag'] == _ns('footnote'):
                yield dict(type=ev.TEXT, text=']]')
            elif peer['tag'] == _ns('anchor'):
                pass
            elif peer['tag'] == _ns('disp'):
                pass
            elif peer['tag'] == _ns('img'):
                pass
            else:
                assert False, obj
        else:
            assert obj['type'] == ev.TEXT
            yield obj


def md_text(p, prefix=None):
    if prefix:
        yield prefix + ' '
    for obj in md(ev.scan(p)):
        yield obj['text']


def md_block(p):
    if p.tag == _ns('p'):
        if len(p) > 0 and p[0].tag == _ns('small'):
            assert not p.text
            assert len(p) == 1
            assert not p[0].tail

            return ''.join(md_text(p[0], '###'))
        else:
            return ''.join(md_text(p))
    elif p.tag == _ns('anchor'):
        return ''.join(md_text(p))
    else:
        assert False, p.tag


def format_lines(text, max_line_len=80):
    tokens = text.split()
    line_len = 0
    for tk in text.split():
        if line_len + 1 + len(tk) > max_line_len:
            yield '\n'
            yield tk
            line_len = len(tk)
        else:
            if line_len:
                yield ' '
            yield tk
            line_len += 1 + len(tk)


def normalize_anchor(xml):
    for a in xml.findall('.//' + _ns('anchor')):
        type_ = a.attrib.pop('type')
        number = a.get('number')
        label = a.get('label')
        assert number, et.tostring(a, encoding='utf-8')
        if type_ == 'folio':
            if label is None:
                assert False, et.tostring(a, encoding='utf-8').decode()
                a.attrib['label'] = number
            if number[-1] == 'v':
                number = int(number[:-1]) * 2
            else:
                number = int(number) * 2 - 1
            a.attrib['number'] = str(number)
        elif type_ == 'page':
            if label is None:
                a.attrib['label'] = number
        else:
            assert False, et.tostring(a, encoding='utf-8')


def convert(fname):

    with open(fname, 'r', encoding='utf-8') as f:
        xmltext = f.read()
        xmltext = detect_first_letter(xmltext)
        xml = et.fromstring(xmltext.encode('utf-8'))
        normalize_anchor(xml)
        et.strip_tags(xml, _ns('footer'), et.Comment)

        for p in xml:
            assert p.tag in (_ns('p'), _ns('anchor')), p.tag
            text = md_block(p)
            text = ''.join(format_lines(text))
            yield text.strip() + '\n\n'


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Converts XML to cu-flavored markdown')
    parser.add_argument('input', help='input XML file')
    parser.add_argument('output', help='output Markdown file')

    args = parser.parse_args()

    with open(args.output, 'w', encoding='utf-8') as f:
        for data in convert(args.input):
            f.write(data)


if __name__ == '__main__':
    main()