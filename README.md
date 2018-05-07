# cumd

Church Slavonic dialect of Markdown

## Markup

1. Use star symbol to mark red spans, for example: `*Слава и ныне*`
2. Use double underscore to mark expanded font: `__Священник глаголет:__`
3. Use leading tilda to mark first letter of a word red: `~Христос рождается`
4. For pagebreak anchors use `<<5: л. 3 об.>>` or simply ``<<5>>`` when label is the same 
   as the page number
5. Use leading curcumflex symbol to mark bukvitsa: `^Вначале было Слово`
6. For verse numbering use `((и))`

This package provides two commands:
* `cumd` - renders markdown into html
* `cuxml` - converts Ponomar XML into markdown

## cumd
```
usage: cumd [-h] [--html] input output

Converts CU markdown to HTML

positional arguments:
  input       File name of the input *.md file
  output      File name of the output *.html file

optional arguments:
  -h, --help  show this help message and exit
  --html      Set to generate viewable HTML
```

## cuxml
```
usage: cuxml [-h] input output

Converts XML to cu-flavored markdown

positional arguments:
  input       input XML file
  output      output Markdown file

optional arguments:
  -h, --help  show this help message and exit
```