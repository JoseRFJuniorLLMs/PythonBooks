# this file demonstrates how to load a previously
# generated grammar object from a file, without
# regenerating the grammar

import DLispShort

# load the previously defined grammar
# and bind the semantics functions
#
LGrammar = DLispShort.LoadLispG()

# do some test derivations
Context = {}

test1 = LGrammar.DoParse1( '(setq var ("this" "value" 10))' , Context)
test2 = LGrammar.DoParse1( '(var (1 3 9) (setq me "aaron"))' , Context)
test3 = LGrammar.DoParse1( '(setq nullstring "")' , Context)
test4 = LGrammar.DoParse1( '(print (var nullstring me))' , Context)
test5 = LGrammar.DoParse1( '((("var" var) (print "so long!")))' , Context)
