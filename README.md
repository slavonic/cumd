# cumd

Church Slavonic dialect of Markdown

## Markup

1. Use `=` symbol to mark red spans, for example: `=Слава и ныне=`
2. Use `+` to mark expanded font: `+Священник глаголет:+`
3. Use leading tilda to mark first letter of a word red: `~Христос рождается`
4. For pagebreak anchors use `<<5: л. 3 об.>>` or simply ``<<5>>`` when label is the same 
   as the page number
5. Use leading curcumflex symbol to mark bukvitsa: `^Вначале было Слово`
6. For verse numbering use `((и))`
7. For footnote use `[[footnote text]]` (Attention: this is likely to change)

This package provides two commands:

* `cumd` - renders markdown into html
* `cuxml` - converts Ponomar XML into markdown

## cumd

```bash
usage: cumd [-h] [--html] [--simplified] [--extensions EXTENSIONS] input output

Converts CU markdown to HTML

positional arguments:
  input                 File name of the input *.md file
  output                File name of the output *.html file

options:
  -h, --help            show this help message and exit
  --html                Set to generate viewable HTML
  --simplified, -s      Set to generate HTML without custom tags
  --extensions EXTENSIONS, -e EXTENSIONS
                        List of comma-separated extensions to enable. For example -e footnotes,math
```

## cuxml

```bash
usage: cuxml [-h] [--max-line-len MAX_LINE_LEN] input output

Converts XML to cu-flavored markdown

positional arguments:
  input       input XML file
  output      output Markdown file

optional arguments:
  -h, --help  show this help message and exit
  --max-line-len MAX_LINE_LEN, -m MAX_LINE_LEN   Line length in generated Markdown (cosmetic)
```
