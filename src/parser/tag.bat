
java -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -genprops > myPropsFile.prop
java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/wsj-0-18-bidirectional-distsim.tagger -textFile input.txt > tagged.txt
