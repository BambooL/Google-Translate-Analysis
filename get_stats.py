import re


f = open('res', 'r+')
university_list = set()
biased_list = set()
unbiased_list = set()
unfavor_list = {}
favor_list = {}
false = 0
while True:
	line = f.readline()
	if not line:
		break
	else:
		if ("is" in line):
			u = line.split(" is")[0]
			university_list.add(u)
		if ("is better than" in line):
			false = false + 1
			u1 = line.split(" is better than ")[0]
			u2 = line.split(" is better than ")[1][:-1]
			biased_list.add(u1)
			biased_list.add(u2)
			if u2 in unfavor_list:
				count = unfavor_list[u2] + 1
				unfavor_list[u2] = count
			else:
				unfavor_list[u2] = 1 
			if u1 in favor_list:
				count = favor_list[u1] + 1
				favor_list[u1] = count
			else:
				favor_list[u1] = 1
for u in university_list:
	if u not in biased_list:
		unbiased_list.add(u)

print "____________________________________________________"
print "Total false number:",
print false
print "____________________________________________________"
print "Unfavor List:"
for key, value in sorted(unfavor_list.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    print "%s: %s" % (key, value)
# print unfavor_list
print "____________________________________________________"
print "Favor List:"
for key, value in sorted(favor_list.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    print "%s: %s" % (key, value)
print "____________________________________________________"
print "Unbiased List:"
print unbiased_list







