import sys
import os
import re
class_location={}
ZeroClass=[]
max_len_add=0;
max_add_word=""
Super_Dict={}
uni_addDict={}
ZeroWords=[]
words_seen_so_far={}
def find(s,ch):
  return [i for i, ltr in enumerate(s) if ltr == ch]

def discard_zero():
  for k in class_location:
    val=class_location[k]
    if ('','') in val:
      val.remove(('','')) 
    if len(val) == 0:
      ZeroClass.append(k)
    #print val
    class_location[k]=val
  pass

def write_zero_word():
  string="\n".join(ZeroWords)
  open("RWords",'w').write(string)    
  pass
def loaderAddDeleteRules(file_name):
  f=open("word_class_rules.ans","w")
  f.write("word\tclass name\t no of add del rules\t no of rules obeyed\t no of words actually in corpus\n")
  f.close()
  f=open(file_name,'r').read()
  class_list=find(f,'$')
  File_list=find(f,'*')
  #print f
  global class_location,ZeroClass;
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
    class_location[f[class1+1: f[class1:].index('\n')+class1]]=list(set(rule_list))
    #if  class_location[f[class1+1: f[class1:].index('\n')+class1]]==[('','')]:
          #print #ZeroClass.append(f[class1+1: f[class1:].index('\n')+class1])
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
  global Super_Dict;
  Su=open(dic_path,'r').readlines()
  for word in Su:
    Super_Dict[word[:-1]]=''
  pass
def wirte_in_file1(word,dictionary):
  f=open('word_class_rules.ans','a+')
  for k in dictionary:
    if k not in ZeroClass:
    #print 
      v=dictionary[k]
    #print v
      (no_rules,actual_rules)=(v[0],v[1])
      if actual_rules != 0:
        a=0
	#print "##"+word 
      f.write(word+"\t"+str(k)+"\t"+str(len(class_location[k]))+"\t"+str(no_rules)+"\t"+str(actual_rules)+"\n")
  f.close()
  pass
  
def found_in_corpus(word):
  global Super_Dict;
  #print Super_DictSA
  #print word
  no=0
  for i in word:
    #print i
    if i in Super_Dict:
      #print i + "Found"
      no=no+1
  #print "Number of words found in corpus : "+str(no)+ "out of "+str(len(word))
  if no == len(word):
  #print ""
    return (True,no)
  else:
    if no==len(word): # means no word form existed for that particular word in that class.
      print "None of the words present"
    return (False,no)
def main():
  if len(sys.argv) < 4:
    print "1 : Input UNK words in WX form \n 2: Add dele rules \n 3: suff_info \n 4: All words found in corpus"
  load_dictionary(sys.argv[4])
  input_file=open(sys.argv[1],'r').readlines()
  loaderAddDeleteRules(sys.argv[2])
  input_file_list=[]
  file_new=open('words_classes','w')
  file_new.close()
  file_new=open('words_classes','a')
  fn=open("CompleteList.ans","w")
  fn.close()
  #print class_location
  checkIt=False
  for i in input_file:
    input_file_list.append(i[:-1][::-1])
  # string stores the word in reverse, temp_word has the suffix-less-word(but still reve)
  discard_zero()
  global ZeroWords
  #print class_location
  for string in input_file_list:
    dict_class_word_formed={}
    for leng in range(0,max_len_add):
      break_from_class=False
      dict_class_no_rules_agreed={}
      if string[:leng] in uni_addDict:
        temp_word=string[leng:]
        add_list=uni_addDict[string[:leng]]
        for tup in add_list:
          re_tup0=tup[0][::-1]
          temp1=re_tup0+temp_word
	  #reverseing the add part so that we can get right root ie temp1          
	  temp1=temp1[::-1]
          #print "I am a generated word:  "+temp1
	  if found_in_corpus([temp1])[0]:
	    try:
	      list_del_add_rule=class_location[tup[1]]
              len_rules=len(list_del_add_rule)
	      words_formed=[]
	    except KeyError:
	      continue; 
	    for r_tup in list_del_add_rule:
	        end_string=temp1[-len(r_tup[0]):]
		if end_string == r_tup[0] or  len(temp1) == len(end_string):
		  if len(r_tup[0]) == 0:
        	    words_formed.append(temp1+r_tup[1])
		  else:
		    words_formed.append(temp1[:-(len(r_tup[0]))]+r_tup[1])
	    (see, rule_obeyed)=found_in_corpus(words_formed)
	    dict_class_no_rules_agreed[tup[1]]=(len(words_formed),rule_obeyed)
    	    real_word=string[::-1]
	    #print "look at this ============= "+dict_class_no_rules_agreed
	    if len(words_formed)==len_rules:
	      #print "Matched all the rules,Yey, the word was "+string+ "Root form was "+temp1
	      #print "Sending the words formed out of it to check if they are in corpus "
	      if see:
		checkIt=True
		if real_word in words_seen_so_far:
     		  checkIt=False
	        #print "The class for this has been found now no need to search anymore!!, class is"+tup[1]
		#file_new.write(real_word+"\t"+tup[1]+"\n")
		if len(words_formed)==0: #and words_formed[0]==temp1:
		  a=0
			#print real_word +"\t"+tup[1] PROBABLY ZERO CLASS
		  #print "word :" +string[::-1] + "\tclass found :"+tup[1]
		else:
		  if tup[1] not in dict_class_word_formed:
		    dict_class_word_formed[tup[1]]=words_formed
		  if real_word not in words_seen_so_far:
		    file_new.write(real_word+"\t"+tup[1]+"\n")
		#break_from_class=True
		#break 
	        #print "checking for other class"
            if real_word not in words_seen_so_far:
	      ZeroWords.append(real_word)
              ZeroWords=list(set(ZeroWords))
              if dict_class_no_rules_agreed[tup[1]][1] !=0:
	        ZeroWords.remove(real_word) 	
	  #else:
	    #print "Root in not in corpus"+temp1   
      #if break_from_class:
        #break;
      #print "word ::: "+ string[::-1] 
      #print dict_class_no_rules_agreed
      if string[::-1] not in words_seen_so_far:
        wirte_in_file1(string[::-1],dict_class_no_rules_agreed)
      if checkIt:
        del_it=[]
 	
        list_d=dict_class_word_formed.items()
        #print string[::-1]
	#print "This is the list_d contains a list of something" #
	#print list_d
        for i in range(0,len(dict_class_word_formed)):
	  for j in range (i+1,len(dict_class_word_formed)):#  dict_class_word_formed:
	    #dict_class_word_formed[k1]
 	    #print list_d[i][1]
            if list_d[i][1]==list_d[j][1] : 
	      print "I was same as the other"
              del_it.append(list_d[i])
            if list_d[i][1]!=list_d[j][1] and set( list_d[i][1] ).issuperset( set( list_d[j][1])): 
	      del_it.append(list_d[j])
	    if list_d[i][1]!=list_d[j][1] and set( list_d[j][1] ).issuperset( set( list_d[i][1])):
	      del_it.append(list_d[i])
	
	#if len(list_d) != 0:
          #open("CompleteList.ans","a").write(string[::-1]+"\t"+)      
        #print string[::-1]
        #print dict_class_word_formed
        for c in del_it:
	  if c in list_d:
	    list_d.remove(c)
	if len(list_d) != 0:
	  words_seen_so_far[string[::-1]]=''
	  for t in list_d:
	    for forms in t[1]:
	      words_seen_so_far[forms]='' 
          open("CompleteList.ans","a").write(string[::-1]+"\t"+ str(list_d)+"\n")      
        #print string[::-1]
        #print list_d
      checkIt=False
      
  	    

if __name__ == '__main__':
  main()
  ZeroWords.sort()
  #print ZeroWords
  write_zero_word()

