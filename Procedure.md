Steps for execution of the project files:

Step 1:
 - Download the enron email dataset from http://www.cs.cmu.edu/~enron/
 - Unzip the files and paste them in the src/enron_mail/maildir/ directory
 - For reference, check the sampe emails of a single person present in this repository
 
Step 2:
 - Download the stanford parser from http://nlp.stanford.edu/software/lex-parser.shtml
 - Download the stanford pos tagger from http://nlp.stanford.edu/software/tagger.shtml
 - Unzip the files and paste them in the src/parser/ directory

Step 3:
 - Download supporting files from http://www.slf4j.org/download.html
 - Unzip and paste them in the src/parser/ directory

Step 4:
 - Calcuate the dependency pairs using the parser and replace the tags of the respective tokens using tagger to get dependecny pairs of pos tags.
 - These are the most important features used in this project
