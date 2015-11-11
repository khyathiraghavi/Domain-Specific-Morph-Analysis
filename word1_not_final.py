import sys
import os
import re
class_location={}
pclass=[]
max_len_add=0;
max_add_word=""
Super_List=[]
def find(s,ch):
  return [i for i, ltr in enumerate(s) if ltr == ch]

def loaderAddDeleteRules(file_name):
  f=open(file_name,'r').read()
  class_list=find(f,'$')
  File_list=find(f,'*')
  #print f
  global class_location;
  for class1 in class_list:
    #class_location[f[class1+1: f[class1:].index('\n')+class1]]=f[class1:].index('\n')+class1+1
    start_loc=f[class1:].index('\n')+class1+1
    end_loc=f[class1:].index('\n\n')+class1+1
    #temp_l=f[start_loc:end_loc].split()
    temp_l=re.findall(r"[\w']+",f[start_loc:end_loc])
    le=len(temp_l)    
    rule_list=[]
    #print le
    #print temp_l
    i=0
    while i < le:
     # print i
      #a if test else b
      delete1='' if temp_l[i]== str(0) else temp_l[i]
      #print "has to be removed "+ delete1+"."
      add1='' if temp_l[i+1]== str(0) else temp_l[i+1]
      rule_list.append((delete1,add1))
      i=i+2
    class_location[f[class1+1: f[class1:].index('\n')+class1]]=rule_list
  os.system("cut -f1-4 -d',' "+sys.argv[3]+" >newer_suff_info")
  f1=open('newer_suff_info','r')
  line=f1.read()
  li=re.split(r",|\n", line)
  li=li[:-1]
  counter=0
  global uni_addDict;
  uni_addDict={}
  global add, delete, pclass, max_len_add, max_add_word;
  c=0
  while c < len(li):
    c=c+4
  while counter< len(li): 
    addition=li[counter+1]
    removal=li[counter]
    if li[counter] in uni_addDict:
      tup=(addition, li[counter+2]+"&"+li[counter+3])
      uni_addDict[li[counter]].append(tup)
    else:
      if max_len_add < len(li[counter]):
        max_len_add=len(li[counter])
        max_add_word=li[counter]	
      uni_addDict[li[counter]]=[(addition, li[counter+2]+"&"+li[counter+3])]
    counter=counter+4
  #print uni_addDict
  pass
def load_dictionary(dic_path):
  global Super_List;
  Su=open(dic_path,'r').readlines()
  for word in Su:
    Super_List.append(word[:-1])
  pass
def found_in_corpus(word):
  global Super_List;
  #print Super_List
  print word
  for i in word:
    print i
    if i not in Super_List:
      return True #			CHANGE THIS TO False
  print "I am found"
  return True
def main():
  if len(sys.argv) < 4:
    print "1 : Input UNK words in WX form \n 2: Add dele rules \n 3: suff_info \n 4: All words found in corpus"
  load_dictionary(sys.argv[4])
  input_file=open(sys.argv[1],'r').readlines()
  loaderAddDeleteRules(sys.argv[2])
  input_file_list=[]
  for i in input_file:
    input_file_list.append(i[:-1][::-1])

  for string in input_file_list:
    for leng in range(0,max_len_add):
      break_from_class=False
      if string[:leng] in uni_addDict:
	print " This was found in the Dic !! "+ string[:leng]+"."
        temp_word=string[leng:]
        add_list=uni_addDict[string[:leng]]
        for tup in add_list:
	  print "The word is "+temp_word
          #print "tup[0] ie what is to be added :"+tup[0]
          temp1=tup[0]+temp_word
	  temp1=temp1[::-1]
          print "I am a generated word:  "+temp1
	  if found_in_corpus([temp1]):
	    list_del_add_rule=class_location[tup[1]]
            len_rules=len(list_del_add_rule)
	    words_formed=[]
	    for r_tup in list_del_add_rule:
	        end_string=temp1[-len(r_tup[0]):]
		if end_string == r_tup[0] or  len(temp1) == len(end_string):
		  if len(r_tup[0]) == 0:
		    #means nothing to add
        	    words_formed.append(temp1+r_tup[1])
		    print temp1+r_tup[1]
		  else:
		    words_formed.append(temp1+r_tup[1])
		    print temp1[:-(len(r_tup[0]))]+r_tup[1]
		else:
		  print "It dint match the last char"
	    print " the number of rules satisfied == "+str(len(words_formed))
	    if len(words_formed)==len_rules:
	      print "Matched all the rules,Yey, the word was "+string+ "Root form was "+temp1
	      print "Sending the words formed out of it to check if they are in corpus "
	      if found_in_corpus(words_formed):
	        print "The class for this has been found now no need to search anymore!!, class is"+tup[1]
		print "word :" +string + "\troot:"+tup[1]
		break_from_class=True
		break;
	    else:
	       print "checking for other class"	
	  else:
	    print "Root in not in corpus"   
      if break_from_class:
        break;
		
	    

if __name__ == '__main__':
  main()

