from cumd.cumd import cumd


def test_smoke():
    result = cumd('''
# Hello
~Some text with ~some red bukvas
''')
    assert result == '''<h1>Hello</h1>
<p><red>S</red>ome text with <red>s</red>ome red bukvas</p>\
'''

def test_digraph():
    result = cumd('''
~Оу҆слы́шахъ, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '<p><red>Оу҆</red>слы́шахъ, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...</p>'

def test_wide():
    result = cumd('''
__~Оу҆слы́шахъ__, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><wide><red>Оу҆</red>слы́шахъ</wide>, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_red():
    result = cumd('''
*Оу҆слы́шахъ*, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><red>Оу҆слы́шахъ</red>, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_red_wide():
    result = cumd('''
*__Оу҆слы́шахъ__, гдⷭ҇и*, смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><red><wide>Оу҆слы́шахъ</wide>, гдⷭ҇и</red>, смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_wide_red():
    result = cumd('''
__Оу҆слы́шахъ, *гдⷭ҇и*__, смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><wide>Оу҆слы́шахъ, <red>гдⷭ҇и</red></wide>, смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_anchor():
    result = cumd('''
__Оу҆слы́шахъ, *гдⷭ҇и*__, <<84>>смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><wide>Оу҆слы́шахъ, <red>гдⷭ҇и</red></wide>, <anchor label="84" page="84"></anchor>смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_verse_anchor():
    result = cumd('''
__Оу҆слы́шахъ, *гдⷭ҇и*__, ((i))смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><wide>Оу҆слы́шахъ, <red>гдⷭ҇и</red></wide>, <verse label="i"></verse>смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''
