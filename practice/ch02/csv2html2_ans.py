#!/usr/bin/env python

import sys
import xml.sax.saxutils 

def main():
    maxwidth, format_type = process_options()
    if maxwidth==None: sys.exit()
    print_start()
    count = 0
    while True:
        try:
            line = raw_input()
            if count == 0:
                color = "lightgreen"
            elif count % 2:
                color = "white"
            else:
                color = "lightyellow"
            print_line(line, color, maxwidth, format_type)
            count += 1
        except EOFError:
            break
    print_end()

def process_options():
    maxwidth = 100
    format_type = ".0f"
    if len(sys.argv)==2 and sys.argv[1] in ["-h", "--help"]:
        print """\
        usage: csv2html.py [maxwidth=int] [format=str] < infile.csv > outfile.html

        maxwidth is an optional integer; if specified, it sets the maximum
        number of characters that can be output for string fields,
        otherwise a default of 100 characters is used.

        format is the format to use for numbers; if not specified it
        defaults to ".0f" """
        return None, None
    elif len(sys.argv)==1:
        return maxwidth, format_type
    for argv in sys.argv[1:]:
        if "maxwidth" in argv:
            maxwidth = int(argv[argv.index("=")+1:])
        elif "format" in argv:
            format_type = argv[argv.index("=")+1:]
        else:
            print "Have some error! Please use flag [-h] or [--help] to see usage"
            return None, None
    return maxwidth, format_type
     

def print_start():
    print("<table border='1'>")

def print_line(line, color, maxwidth, format_type):
    print("<tr bgcolor='{0}'>".format(color))
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("<td></td>")
        else:
            number = field.replace(",", "")
            try:
                x = float(number)
                print("<td align='right'>{0:{1}}</td>".format(round(x), format_type))
            except ValueError:
                field = field.title()
                field = field.replace(" And ", " and ")
                if len(field) <= maxwidth:
                    field = xml.sax.saxutils.escape(field)
                else:
                    field = "{0} ...".format(xml.sax.saxutils.escape(field[:maxwidth]))
                print("<td>{0}</td>".format(field))
    print("</tr>")

def extract_fields(line):
    fields = []
    field = ""
    quote = None
    for c in line:
        if c in "\"'":
            if quote is None: # start of quoted string
                quote = c
            elif quote == c:  # end of quoted string
                quote = None
            else:
                field += c    # other quote inside quoted string
            continue
        if quote is None and c == ",": # end of a field
            fields.append(field)
            field = ""
        else:
            field += c        # accumulating a field
    if field:
        fields.append(field)  # adding the last field
    return fields




def print_end():
    print("</table>")

main()
