#!/usr/bin/env python

import os
import sys


def main():

    dirty = False
    items = []

    filename = load_file()

    line_num = -1
    try:
        for line_num, line in enumerate(open(filename, 'rw'), start=1):
            if line_num != -1:
                items.append(line)
    except IOError:
        pass

    while True:
        if len(items) == 0:
            print "-- no items are in the list --"
            s = option_chose('add_only')
        else:
            print_items(items)
            s = option_chose()
        dirty = deal_option(s, dirty, items, filename)


def load_file():
    file_list = [filename for filename in os.listdir('.') if filename.endswith('.lst')]
    fn_num = 0
    if file_list:
        for idx, fn in enumerate(sorted(file_list), start=1):
            print idx, fn
        fn_num = get_integer("Specify file's number (or 0 to create a new one)", "filename number", maximum=idx)
        if fn_num != 0: filename = file_list[fn_num-1]

    if not file_list or fn_num == 0:
        filename = get_string("Choose filename", "filename")
        if not filename.endswith('.lst'): filename += '.lst'
    return filename


def print_items(items):
    for line_num, line in enumerate(items, start=1):
        print "{0:4}: {1}".format(line_num, line.strip())


def option_chose(option='all'):

    if option=='add_only':
        input_msg = "[A]dd [Q]uit (default:[A])"
        choise_str = "AaQq"
    else:
        input_msg = "[A]dd [D]elete [S]ave [Q]uit (default:[A])"
        choise_str = "AaDdSsQq"

    while True:
        result = get_string(input_msg, maximum_length=1)
        if result in choise_str:
            return result
        else:
            print "ERROR: invalid choice--enter one of '{0}'".format(choise_str)
            raw_input("Press Enter to continue...")


def deal_option(s, dirty, items, filename):
    if s == '': s = 'a'

    if s.lower() == 'a':
        item_str = get_string("Add item")
        items.append(item_str)
        items.sort(key=str.lower)
        dirty = True
    elif s.lower() == 'd':
        item_num = get_integer("Delete item number (or 0 to cancel)", maximum=len(items))
        if item_num !=0:
            del items[item_num-1]
            dirty = True
    elif s.lower() == 's':
        save_list(filename, items)
        dirty = False
    elif s.lower() == 'q':
        if dirty:
            save_chose = get_string("Save unsaved changes (y/n)")
            if save_chose.lower() in 'yes ':
                save_list(filename, items)
                dirty = False
        else:
            sys.exit()
    return dirty


def save_list(fn, items):
    with open(fn, 'w') as fd:
        for line_num, line in enumerate(items, start=1):
            fd.write("{0}\n".format(line))
        print "Saved {0} item{2}to {1}".format(len(items), fn, ('s ' if len(items) > 1 else " "))
        raw_input("Press Enter to continue...")


def get_string(message, name="string", default=None, minimum_length=0, maximum_length=80):
    message += ': '

    while True:
        try:
            string = raw_input(message)
            if not (minimum_length <= len(string) <= maximum_length):
                raise ValueError("{name} must have at least {minimum_length} and at most {maximum_length} characters".format(**locals()))
            return string
        except ValueError as err:
            print "ERROR", err


def get_integer(message, name="integer", default=None, minimum=0, maximum=100, allow_zero=True):

    message += ': '

    class RangeError(Exception): pass

    while True:
        try:
            number = input(message)
            if not (minimum <= number <= maximum):
                raise RangeError("{name} must be between {minimum} and {maximum} .".format(**locals()))
            if not allow_zero and number==0:
                raise RangeError("{name} can not be zero.".foramt(**locals()))
            return number
        except NameError as err:
            print "ERROR", err
        except RangeError as err:
            print "ERROR", err


main()
