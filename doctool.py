# Copyright (C) 2011 Edgeware AB.
# All Rights Reserved.

"""Small utility to build a single document from multiple
Markdown files.
"""

import markdown
import jsontemplate
import os.path
import re
import sys

html_wrap = """\
<html>
  <head>
    <style type="text/css" media="print">
      {print_css}
    </style>
    <style type="text/css" media="screen">
      {screen_css}
    </style>
  </head>
  <body>
    {content}
  </body>
</html>
"""

reference_regexp = re.compile("\[.+\]\((.*)\.html\)")

include_regexp = re.compile("<!--include (.*)-->")

headerid_regexp = re.compile("^#+ (.+) {(.+)}", re.MULTILINE)

header_regexp = re.compile("^(#+) (.+)", re.MULTILINE)

internal_link_regexp = re.compile("(\[\]\((#.+?)\))")


def _find_files(seen, filename):
    seen.append(filename)
    text = open(filename).read().decode('utf-8')
    files = include_regexp.findall(text)
    for refname in files:
        path = os.path.join(os.path.dirname(filename), refname)
        if not path in seen:
            _find_files(seen, path)


def _resolve_internal_links(text):
    anchors = {}
    for m in headerid_regexp.finditer(text):
        anchor, title = m.group(2), m.group(1)
        if anchor in anchors:
            raise ValueError("Anchor already exists: %s" % anchor)
        anchors[anchor] = title
        text = text.replace('{' + anchor + '}', '')

    for r in internal_link_regexp.finditer(text):
        link, anchor = r.group(), r.group(2)
        if not anchor in anchors:
            raise ValueError("Unresolved internal link: " + anchor)

        resolved_link = "[%s](%s)" % (anchors[anchor], anchor)
        text = text.replace(link, resolved_link, 1)

    return text


def _number_headers(text):
    ALPHA_MARKER = '[@]'

    def _inc(s):
        return str(int(s) + 1) if s.isdigit() else chr(ord(s) + 1)

    nums = ['0']  # ['1', '2'] = 1.2, ['A', '2', '1'] = A.2.1
    alpha_mode = False
    for m in header_regexp.finditer(text):
        orig_header, hashes, title = m.group(), m.group(1), m.group(2)
        level = len(hashes)

        if level == len(nums):
            nums[-1] = _inc(nums[-1])  # 1.1 -> 1.2
        elif level > len(nums):
            nums.append('1')           # 1.2 -> 1.2.1
        else:
            nums = nums[:level]
            nums[-1] = _inc(nums[-1])  # 1.2.3 -> 2

        if ALPHA_MARKER in title:
            if not alpha_mode:
                nums[0] = 'A'
            alpha_mode = True
            header = orig_header.replace(ALPHA_MARKER, ".".join(nums))
        else:
            num_str = ".".join(nums) if level != 1 else ".".join(nums) + "."
            header = "%s %s %s" % (hashes, num_str, title)
        text = text.replace(orig_header, header, 1)

    return text


def _convert(files):
    text = []
    for filename in files:
        text.append(open(filename).read().decode('utf-8'))
    text = include_regexp.sub('', ''.join(text))
    text = _number_headers(text)
    text = _resolve_internal_links(text)
    md = markdown.Markdown(
        extensions=[
                'toc', 'def_list', 'headerid', 'tables', 'graphviz', 'ditaa'],
        output_format='html4',
        extension_configs={
            'graphviz': {},
            'ditaa': {}
        },
    )
    return md.convert(''.join(text))


def _load_css(fname):
    css = open(os.path.join(
            os.path.dirname(__file__), 'style', fname)).readlines()
    return ''.join((' ' * 6) + l for l in css).strip()


def build_single_file(infile, outfile):
    files = []
    _find_files(files, infile)
    text = _convert(files)

    screen_css = _load_css('style.css')
    print_css = _load_css('print.css')

    html = jsontemplate.expand(html_wrap, {
            'content': text,
            'screen_css': screen_css,
            'print_css': print_css
    })
    open(outfile, 'w').write(html.encode('utf-8'))


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) == 2:
        argv.append(os.path.splitext(argv[1])[0] + '.html')
    if len(argv) != 3:
        print "Usage: doctool <infile> [outfile]"
        return 1
    build_single_file(argv[1], argv[2])
    return 0


if __name__ == '__main__':
    sys.exit(main())
