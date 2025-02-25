from cumd.cuxml import convert


def test_smoke():
    data= list(convert('''
<doc xmlns="http://www.ponomar.net/culiturgical">
    <p><red>A</red>foo Hello</p>
</doc>
'''))
    
    assert len(data) == 1
    assert data[0] == "~Afoo Hello\n\n"

def test_red():
    data= list(convert('''
<doc xmlns="http://www.ponomar.net/culiturgical">
    <p><red>Hello</red> word</p>
</doc>
'''))
    
    assert len(data) == 1
    assert data[0] == "=Hello= word\n\n"

def test_underline():
    data= list(convert('''
<doc xmlns="http://www.ponomar.net/culiturgical">
    <p><u>Hello</u> word</p>
</doc>
'''))
    
    assert len(data) == 1
    assert data[0] == "<u>Hello</u> word\n\n"


def test_bold():
    data= list(convert('''
<doc xmlns="http://www.ponomar.net/culiturgical">
    <p><b>Hello</b> word</p>
</doc>
'''))
    
    assert len(data) == 1
    assert data[0] == "<b>Hello</b> word\n\n"


def test_italic():
    data= list(convert('''
<doc xmlns="http://www.ponomar.net/culiturgical">
    <p><i>Hello</i> word</p>
</doc>
'''))
    
    assert len(data) == 1
    assert data[0] == "<i>Hello</i> word\n\n"
