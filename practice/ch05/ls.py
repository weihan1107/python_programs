#!/usr/bin/env python

import optparse

def main():
    parser = optparse.OptionParser(usage="usage: %prog [options] [path1 [path2 [... pathN]]]")
    parser.add_option("-H", "--hidden", action="store_true", default=False, dest="hidden", help="show hidden files [default: off]")
    parser.add_option("-m", "--modified", action="store_true", default=False, dest="modified", help="show last modified date/time [default: off]")
    parser.add_option("-o", "--order", dest="ORDER", help="order by ('name', 'n', 'modified', 'm', 'size', 's') [default: off]")
    parser.add_option("-r", "--recursive", action="store_true", default=False, dest="recursive", help="recurse into subdirectories [default: off]")
    parser.add_option("-s", "--sizes", action="store_true", default=False, dest="sizes", help="show sizes [default: off]")
    opts, args = parser.parse_args()





main()