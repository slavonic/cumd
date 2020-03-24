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

def test_bukvitsa():
    result = cumd('''
^Оу҆слы́шахъ, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '<p><bukvitsa>Оу҆</bukvitsa>слы́шахъ, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...</p>'

def test_wide():
    result = cumd('''
+~Оу҆слы́шахъ+, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><wide><red>Оу҆</red>слы́шахъ</wide>, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_red():
    result = cumd('''
=Оу҆слы́шахъ=, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><red>Оу҆слы́шахъ</red>, гдⷭ҇и, смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_red_wide():
    result = cumd('''
=+Оу҆слы́шахъ+, гдⷭ҇и=, смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><red><wide>Оу҆слы́шахъ</wide>, гдⷭ҇и</red>, смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_wide_red():
    result = cumd('''
+Оу҆слы́шахъ, =гдⷭ҇и=+, смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><wide>Оу҆слы́шахъ, <red>гдⷭ҇и</red></wide>, смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_anchor():
    result = cumd('''
+Оу҆слы́шахъ, =гдⷭ҇и=+, <<84>>смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><wide>Оу҆слы́шахъ, <red>гдⷭ҇и</red></wide>, <anchor label="84" page="84"></anchor>смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_verse_anchor():
    result = cumd('''
+Оу҆слы́шахъ, =гдⷭ҇и=+, ((i))смотре́нїѧ твоегѡ̀ та́инство...
''')
    assert result == '''\
<p><wide>Оу҆слы́шахъ, <red>гдⷭ҇и</red></wide>, <verse label="i"></verse>смотре́нїѧ твоегѡ̀ та́инство...</p>\
'''

def test_alignment_markers():
    result = cumd('''
# Заголовок{{text_align=center}}

Параграф
{{text_align=justify}}
''')
    assert result == '''\
<h1 text_align="center">Заголовок</h1>
<p text_align="justify">Параграф</p>\
'''

def _test_footnote():
    result = cumd('''
Но даждь изводство (избытие) и крепость
''')
    assert result == '''\
<p>Но даждь <footnote style="u">изводство<text>избытие</text></footnote> и крепость</p>\
'''

def test_md_footnote():
    result = cumd('''
^Но даждь изводство[^1] и крепость

[^1]: избытие
''', extensions=['footnotes'])

    assert result == '''\
<p><bukvitsa>Н</bukvitsa>о даждь изводство<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup> и крепость</p>
<div class="footnote">
<hr>
<ol>
<li id="fn:1">
<p>избытие&#160;<a class="footnote-backref" href="#fnref:1" title="Jump back to footnote 1 in the text">&#8617;</a></p>
</li>
</ol>
</div>\
'''
