import sys
import os
import math # cant compute math.comb, since its for py3.8 ughhhhh
import itertools # use "itertools.permutations" to find all possible combinations
import csv
import re
# ---------- INPUTS -----------
# python3 arm.py input.csv 1a.csv 0.5 0.7
if os.path.exists(sys.argv[2]):
    os.remove(sys.argv[2])
output_file = open(sys.argv[2], "a")
sup_percent = float(sys.argv[3])
min_confidence = float(sys.argv[4])
# ---------- FUNCTIONS -----------
# this returns the total possible combinations of a certain num
def get_comb_count(comb_input_str,num):
    count_combs = 0
    perm = itertools.combinations(comb_input_str,num)
    for i in list(perm): 
        count_combs+=1
    return count_combs
# get actual combs
def get_comb_sets(items,num):
    perm = itertools.combinations(items,num)
    return list(perm)
# ---------- MAIN -----------
total_trans = 0 # get total transactions
element_set = set() # get all unique values
for lines in open(sys.argv[1],"r"): # load initial values
    lines = lines.replace("\n","")
    lines = lines.split(",")
    total_trans += 1
    for i in range(1,len(lines)):
            element_set.add(str(lines[i]))
element_set = sorted(element_set) #sort the set to make it look better
total_combs = get_comb_count(element_set,1) # determine how many loops need to take
total_dict = dict() # the dictionary which holds everything
# do loops for S and R
for looper in range(1,total_combs+1):
    if looper in range(2,total_combs): # if this is not the first loop, update the element_set first, get new combs
        temp_element_set = get_comb_sets(element_set, looper)
        element_set = sorted(temp_element_set)
    element_dict = dict()
    for items in element_set:
        element_dict[items] = int(0)
    if looper == 1: # count frequency
        for lines in open(sys.argv[1],"r"):
            lines = lines.replace("\n","")
            lines = lines.split(",")
            for i in range(1,len(lines)):
                for k,v in element_dict.items():
                    if(k==lines[i]):
                        element_dict[k] = v+1 # increment frequency by 1
    else:
        for k,v in element_dict.items():
            k1 = ''.join(k) #convert tuples to string
            for lines in open(sys.argv[1],"r"):
                all_in = True
                for items in k1:
                    if items not in lines:
                        all_in = False
                if(all_in):
                    v = v+1
                    element_dict[k] = v
    # remove all non-freq values
    # Another way is to use list to force a copy of the keys to be made
    for i in list(element_dict):
        total_dict[i] = float(element_dict[i]/total_trans)
        if(float(element_dict[i]/total_trans)<sup_percent):
            element_dict.pop(i) # pop infreq ones
        else:
            element_dict[i] = float(element_dict[i]/total_trans) # replace frequency to float
    # write to document, force 4 digits after deci
    for k,v in element_dict.items():
        k = re.sub(r'\W+', '', str(k)) # strip all non-numberic/alphabetic values
        temp_out_str = ""
        for items in k:
            temp_out_str += ","
            temp_out_str += str(items)
        output_file.write("S,"+str('%.4f'%v)+temp_out_str+"\n")
    element_set2 = set()
    # update set
    for i in str(element_set):
        for k,v in element_dict.items():
            k1 = ''.join(k)
            for items in k1:
                if(i==items):
                    element_set2.add(i)
                    break
    element_set = sorted(element_set2)
# calculate confidence!
perm_set = set()
conf_dict = dict()
for k,v in total_dict.items():
    perm_set.add(k)
perm = itertools.permutations(perm_set,2)
temp_set = set()
for i in list(perm):
    x = re.sub(r'\W+', '', str(i[1]))
    half_y = re.sub(r'\W+', '', str(i[0]))
    #print(half_y)
    all_in = False
    for items in x:
        if(items in half_y):
            all_in = True
    if not(all_in):
        temp_set.add(i)
# use front -> after
for i in list(temp_set):
    a = re.sub(r'\W+', '', str(i[0]))
    b = re.sub(r'\W+', '', str(i[1]))
    a_b = tuple(re.sub(r'\W+', '', str(sorted(a+b))))
    #print(str(a)+"=>"+str(b))
    if(len(b)!=1):
        b = tuple(b)
    if(len(a)!=1):
        a = tuple(a)
    if a_b in total_dict.keys():
        top = float(total_dict[a_b])
        #print(top)
        if b in total_dict.keys():
            under = float(total_dict[b])
            #print(under)
        if(min_confidence<=float(top/under))and(sup_percent<=top):
            str_to_write = "R,"+str('%.4f'%top)+","+str('%.4f'%float(top/under))+","+str(','.join(b))+",\'=>\',"+str(','.join(a))+"\n"
            output_file.write(str_to_write)