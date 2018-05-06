# cumd

Church Slavonic dialect of Markdown

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