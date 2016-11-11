#!/usr/bin/env python

number_list = []
count = 0

while True:
    try :
        num = input("Enter a number or Enter to finish: ")
        number_list.append(num)
        count +=1
    except SyntaxError:
        break

print "number: ", number_list
print "count =", count, "sum =", sum(number_list), "lowest =", min(number_list), "highest =", max(number_list), "mean =", sum(number_list)/float(count)
