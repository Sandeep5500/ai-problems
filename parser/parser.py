import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red" | "torn"
Adv -> "down" | "here" | "never" 
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she" | "fool" | "masks"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat" | "wears"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """

S -> NP VP | NP VP Conj SS |  NP VP P SS
SS -> SS Conj SS | NP VP | VP | SS P SS 

AP -> Adj | Adj AP
NT -> Det N | N

NP -> NT | AP NT | Det AP NT |  NP PP

PP -> P NP | P
VP -> VP2 | VP2 Adv
VP2 -> VT | VT NP | VT PP 
VT ->  Adv V | V 

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.lower()
    temp_list = nltk.word_tokenize(sentence)
    ret_list = []

    for word in temp_list:
        for letter in word:
            if letter.isalpha():
                ret_list.append(word)
                break

    return ret_list

    # raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # print(tree.flatten())
    # if tree.label() == "S":
        # print("Working")
    npc_list =[]
    for s in tree.subtrees():
        npc = False
        # print(s.label())
        if s.label() == "NP":
            npc = True
            for ss in s.subtrees():
                if ss.label() == "NP" and ss !=s:
                    npc = False 
                    break
        if npc == True:
            npc_list.append(s)

    return npc_list            
    # raise NotImplementedError


if __name__ == "__main__":
    main()
