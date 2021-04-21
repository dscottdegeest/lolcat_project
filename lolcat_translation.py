"""
Program Docstring:

This .py file converts a text file from English to LOLspeak.

Arugments:
a filepath name for a .txt file named *.txt

Output: 
an output file named *_lolcat.txt

Notes:
    This program converts all words to lowercase values.
    This program thus does not preserve capitalization.
    This program does not preserve tab indentations.
    This program conserves the following punctuation marks:
    [',','.',';',':', '?', '!']
    This program adds additional spaces around quotation marks and parenthetical marks.
    Example string: 'The cat said, 'I have a cheeseburger.''
    Translated string: teh kitteh sed, ' i has cheezburger.'

Steps (map out what needs to happen in plain words):
    
    Step 1: the program pulls in the lolcat dictionary
    Step 2: the program asks you to provide a file location and pull that .txt file in
    Step 3: the program defines a function that translates a line of text into lolcat 
    Step 4: the program translates line files then places them in a new list
    Step 5: the program writes each item in the new list to a new .txt file with "_lolcat.txt"

"""

import json
import requests
import pandas as pd

"""
STEP 1: get the lolcat dictionary 
This code grabs the .json from the LOLcatz github page 
url = 'https://github.com/normansimonr/Dumb-Cogs/blob/master/lolz/data/tranzlashun.json'
"""

#identifies location of lolcat dictionary
url_raw = 'https://raw.githubusercontent.com/normansimonr/Dumb-Cogs/master/lolz/data/tranzlashun.json'
#uses requests to get the file transfered
r = requests.get(url_raw)
#reads the file in as a lolcat dictionary
lolcat_dict = r.json()
    
"""
STEP 2 : Pull in files from a location and convert to an object Python can manipulate
"""
def i_can_haz_lolcat(file_name): 
    """
    pulls in a local .txt file and converts it into a list of lines
    
    arguments:
    a file path.
    
    output:
    a list of line strings from that .txt file.
    """
    
    eng_file = open(file_name, 'r')
    
    list_of_lines = eng_file.readlines()
    
    #testing_tool: pulls in only first 250 lines from the .txt file for quicker runs
    #list_of_lines = list_of_lines[0:250]
    
    return list_of_lines
    
'''
STEP 3 : Parse a string file, convert to lolcat, and send to a list  
'''

def convert_to_lolcat(line): 

    import pandas as pd
    
    #call the lolcat dictionary
    #get_lolcat_dict()
    
    #punctuation lists needed for later string manipulation 
    #note that I probably could have used nltk for tokenization to get these handled better
    #also, a regex expression might have been a good option that involved less code
    #but something like re.findall() would omit the punctuation
    
    punctuation = [',', '.', ';', ':', '?', '!', 
                   '(', ')', '[', ']', '{', '}'
                  ]
    
    punctuation_starting = ['(', '[', '{',
                            '\'', '\"'
                           ]
    
    punctuation_quotation = [',\"', ',\'', '\",', '\',',
                             '.\"', '.\'', '\".', '\'.',
                             ';\"', ';\'', '\";', '\';',
                             ':\"', ':\'', '\":', '\':',
                             '?\"', '?\'', '\"?', '\'?', 
                             '!\"', '!\'', '\"!', '\'!',
                            ]
    
    punctuation_parens = ['.)', ').',
                          ',)', '),',
                          '):', ':)',
                          ');', ';)',
                          ')?', '?)',
                          ')!', '!)',
                          ')\"', '\")',
                          ')\'', '\')',
                          '.]', '].',
                          ',]', '],',
                          ']:', ':]',
                          '];', ';]',
                          ']?', '?]',
                          ']!', '!]',
                          ']\"', '\"]',
                          ']\'', '\']',
                          '((', '))',
                          '{{', '}}',
                          '[[', ']]',
                          '(\'', '\')',
                          '{\'', '\'}',
                          '[\'', '\']',
                          '(\"', '\")',
                          '{\"', '\"}',
                          '[\"', '\"]'
                         ]
    
    string_list = line.lower() #converts a line to lowercase
    string_list = string_list.split() #splits lines into words by whitespace
    
    eng_strings = [] #this is an empty list where the translated items will go 
    
    #this block separates items from a line and converts to a list of strings to be compared against the lolcat dictionary
    #this block also addresses issues with punctuation that limit the translation process.
    #in general these blocks tokenizes tarting or ending punctuation.
    #leaving the word that needs to be translated separate from punctuation
 
    for item in string_list: 
        #this if is for a word starts and ends with double-punctuation. Examples: ((cat)) , "(cat)"
        if (item[-2:] and item[:2]) in punctuation_parens and len(item) > 4: 
            eng_strings.append(item[:2])
            eng_strings.append(item[2:(len(item)-2)])
            eng_strings.append(item[-2:])
        #this elif is for a word encased in single punctuation. Examples: (cat), 'cat'
        elif item[0] in punctuation and item[-1] in punctuation and len(item) > 1: 
            eng_strings.append(item[0])
            eng_strings.append(item[1:(len(item)-1)])
            eng_strings.append(item[-1])
        #this elif is for words that start with a single punction. Examples: 'cat, (cat
        elif item[0] in punctuation_starting:
            eng_strings.append(item[0])
            eng_strings.append(item[-(len(item)-1):])
        #this elif is for words that end with double punctuation. Examples: cat). cat,)
        elif item[-2:] in punctuation_quotation: 
            eng_strings.append(item[0:(len(item)-2)])
            eng_strings.append(item[-2:])
        #this elif is for words that end in double parentheticals. Examples: cat)), cat])
        elif item[-2:] in punctuation_parens: 
            eng_strings.append(item[0:(len(item)-2)])
            eng_strings.append(item[-2:])
        #this elif is for words that end in single punctuation. Examples: cat, , cat.
        elif item[-1] in punctuation:
            eng_strings.append(item[0:(len(item)-1)])
            eng_strings.append(item[-1])
        #this elif is for words that end in a single possessive. Examples: cat's
        elif item[-2:] == '\'s':
            eng_strings.append(item[0:(len(item)-2)])
            eng_strings.append(item[-2:])
        #this else is for words with no surrounding punctuation
        else:           
            eng_strings.append(item)


    #this line converts the list to a pandas series
    #then it replaces values via the lolcat dictionary
    #then it converts the pandas series to a list
    lolcat_list = pd.Series(eng_strings).replace(lolcat_dict).tolist()
    
    #this line filters out the empty items created by replacing 'a' with '' from the lolcat dictionary
    lolcat_list = list(filter(None,lolcat_list))
    
    #this line joins the list of strings back together with ' '.
    lolcat_line = ' '.join(lolcat_list)
    
    #many of the items in the string come in with odd punctuation. 
    #Examples: 'cat.' becomes 'kitteh . '
    #these replace statements smooth out many of these issues to make the text more readable.
    lolcat_line = lolcat_line.replace(' ,',',').replace(' .','.').replace(' ;',';')
    lolcat_line = lolcat_line.replace(' :',':').replace(' ?','?').replace(' !','!')
    lolcat_line = lolcat_line.replace(' \'s','\'s')
    lolcat_line = lolcat_line.replace('( ','(')
    lolcat_line = lolcat_line.replace(' )',')')
    lolcat_line = lolcat_line.replace(') ',')')
    
    #this line adds back in the newline that was removed previously.
    lolcat_line = lolcat_line + '\n'
    
    #these are print options and tools for debugging 
    #print(eng_strings) #print the individual word-tokens in English
    #print(lolcat_list) #print the translated-to-lolcat word-tokens
    #print(line) #print the line in English to translate
    #print(lolcat_line) #print the line translated to lolcat
    
    return lolcat_line

"""
STEP 4: the program takes lines from the file, translates them, then puts then in a new list of lines
"""
   
def lolcat_lines():
    """
    Creates a list of the lines to feed into the translator. 
      
    Arguments:
    None.
        
    Outputs:
    `lolcat_lines`: A list of the lines of the dataset that are translated 
        
    Note that this file uses the list_of_lines output from i_can_haz_lolcat()
    """
    
    lolcat_lines = [] #creates an empty list
    
    list_of_lines = i_can_haz_lolcat(file_name) #calls the function that pulls in file to be read
    
    counter = 0 #starts a counter to help track translation progress
    
    #creates a for loop to translate a line of text 
    for row in list_of_lines:
        lolcat_row = convert_to_lolcat(row) #calls the function that translates a line into lolcat
        lolcat_lines.append(lolcat_row) #appends the line to the empty list
        #this print statement updates you on the progress of translating a multiline .txt file
        counter += 1
        print('Line ' + str(counter) + ' of ' + str(len(list_of_lines)) + ' translated')
        
    return lolcat_lines #returns the list of translated lolcat lines 
    
"""
STEP 5 : takes the list of lines and output them to a new .txt file. 
"""
def lolcat_file():
    """
    Save the lines produced by the lolcatlines() function 
    to a file called `filname + lolcat.txt` in the `files` folder.
      
    Arguments:
    None.
      
    Outputs:
    a text file named `filname + lolcat.csv`
    """
    
    #this creates the appropriate file name. 
    #I went with rstrip() over replace() or split() to avoid weird issues with file names
    outfile_name = file_name.rstrip('.txt') + '_lolcat.txt'
     
    #this creates the new file 
    new_file = open(outfile_name, 'w')
    
    #this line calls the lolcat lines function, which iterates over a list of lines to translate into lolcat
    keep_list = lolcat_lines()
           
    #this for loop iterates over the keep list and adds those lines to the _lolcat.txt file
    for record in keep_list:
        new_file.write(record)
        new_file.close     

    print('Your file is ready at the following path: '+ outfile_name)

##################################
### This is where the we get the input of the file path.
##################################

print('Hello. This program takes a .txt file and translates that text into lolcat.')
file_name = input('Please enter a file path for a .txt file to be translated:')

print('Thank you! Beginnning translation process for: '+ file_name)
print('Accessing count by line...')

lolcat_file()
