# Mateo Maramara and Eric Chae
# ICS311 Assignment 2
# This code uses a red black tree with a running time of O(log n) for insertions, deletions, and lookups.
# Instead of using ʻōlelo noʻeau, I used the tree to store Spanish sayings and their English translations the same way.

# Saying object stores both spanish sayings and their English translations.
class Saying:
    def __init__(self, span, eng, sent_span, sent_eng):
        self.spanish = span
        self.english = eng
        self.explanation_spanish = sent_span
        self.explanation_english = sent_eng

# Method to print the Saying object  
    def __str__(self):
        return f"Spanish: {self.spanish}\nEnglish: {self.english}"


# Constants for red and black colors
RED = True
BLACK = False

# Node class for the Red-Black Tree has color attribute and parameter with BST properties.
class RBNode:
    def __init__(self, key, value, color=RED):
        self.key = key #spanish phrase is the key
        self.value = value #Saying object is the value
        self.color = color # property makes the node red or black
        self.left = None #left child
        self.right = None #right child
        self.parent = None #parent node

# Helper function returns if node exists and is red
def isred(node):
    return node is not None and node.color == RED

#Tree class with insert method and fixup method keep bst properties and red black properties
class RBTree:
    def __init__(self):
        self.root = None #Tree is initialized with a empty root node 

    # Insert method to add a new node to the Red-Black Tree
    def insert(self, key, value):
        new_node = RBNode(key, value, color=RED) # create a new node(default red)
        self.bstinsert(new_node) # insert the node with BST properties
        self.fixup(new_node) # fixup to keep red black properties
        self.root.color = BLACK  # ensure the root is always black

    #inserts a new node into the tree while maintaining the Red-Black properties.
    def bstinsert(self, node):
        y = None #Parent node initialized to None
        x = self.root #x traverses the tree from the root
        while x is not None: # Traverse from root until we find a leaf
            y = x
            if node.key < x.key: #Normal BST insertion logic
                x = x.left
            else:
                x = x.right
        node.parent = y #after the loop there will be a parent node which y is pointed to.
        if y is None: # if y is none then tree is empty
            self.root = node # if tree is empty make a root node.
        elif node.key < y.key: #go left or right based on the key using BST logic
            y.left = node
        else:
            y.right = node

    # method to maintain red black properties.
    def fixup(self, node):
        while node != self.root and node.parent.color == RED: #while node is not root and parent is red
            if node.parent == node.parent.parent.left: #if parent is left child
                uncle = node.parent.parent.right # set uncle to the right child of grandparent
                if isred(uncle):  # case 1: if uncle is red
                    node.parent.color = BLACK #parent becomes black
                    uncle.color = BLACK #uncle becomes black
                    node.parent.parent.color = RED #grandparent becomes red
                    node = node.parent.parent #pointer set back to grandparent
                else: #case 2 uncle is black(triangle shape)
                    if node == node.parent.right: # if node is right child(left parent)
                        node = node.parent #set pointer to parent node
                        self.rLeft(node) # rotate left to make a straight line
                    #case 3: node is left child of left parent(form a straight line)
                    node.parent.color = BLACK #parent becomes black
                    node.parent.parent.color = RED #grandparent becomes red
                    self.rRight(node.parent.parent) #rotate right so tree is balanced
            else:  # if parent is right child
                uncle = node.parent.parent.left #uncle is the left child of grandparent
                if isred(uncle):  #case 1:
                    node.parent.color = BLACK #parent becomes black
                    uncle.color = BLACK #uncle becomes black
                    node.parent.parent.color = RED #grandparent becomes red
                    node = node.parent.parent # set pointer to grandparent and continue iteration
                else: #case 2 uncle is black
                    if node == node.parent.left: # if node is left child(right parent)
                        node = node.parent # set pointer to parent node
                        self.rRight(node) # rotate right to make a straight line
                    #case 3
                    node.parent.color = BLACK #make parent black
                    node.parent.parent.color = RED #make grandparent red
                    self.rLeft(node.parent.parent) #rotate left

#rotate left method to keep red black properties
    def rLeft(self, x):
        y = x.right # right child of x
        x.right = y.left # make left child of y the right child of x
        if y.left is not None:
            y.left.parent = x #move pointer of left child to x
        y.parent = x.parent # set parent of y to parent of x
        if x.parent is None:
            self.root = y # if x is root then y becomes root
        elif x == x.parent.left: # if x is left child of parent set y as left child
            x.parent.left = y 
        else: # if x is right child of parent set y as right child
            x.parent.right = y
        y.left = x # set x as left child of y
        x.parent = y #update pointer for x

#rotate right method to keep red black properties
    def rRight(self, x):
        y = x.left # get left child of x
        x.left = y.right # assign y’s right subtree as x’s left subtree
        if y.right is not None:
            y.right.parent = x # update parent pointer of y’s right child to x
        y.parent = x.parent # set y's parent to x's parent
        if x.parent is None:
            self.root = y # if x is root, y becomes new root
        elif x == x.parent.right:
            x.parent.right = y # if x is right child, y replaces x as right child
        else:
            x.parent.left = y # if x is left child, y replaces x as left child
        y.right = x # make x the right child of y
        x.parent = y # update x's parent to y

    # search for a node by key and return its value (Saying object)
    def get(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left # go left if key is smaller
            elif key > node.key:
                node = node.right # go right if key is larger
            else:
                return node.value # key found, return its value
        return None # not found, return None

    #returns true if key exists in the tree
    def member(self, key):
        return self.get(key) is not None

    # returns the first element with the smallest key(spanish sentence)
    def first(self):
        node = self.root
        if not node:
            return None # empty tree
        while node.left:
            node = node.left # go as far left as possible
        return node.value

    #returns the last element with the largest key(spanish sentence)
    def last(self):
        node = self.root
        if not node:
            return None # empty tree
        while node.right:
            node = node.right # go as far right as possible
        return node.value

    # returns the saying just before the current key
    def predecessor(self, key):
        current = self.root
        pred = None
        while current:
            if key > current.key:
                pred = current # update predecessor
                current = current.right
            else:
                current = current.left
        return pred.value if pred else None

    # returns the saying just after the current key
    def successor(self, key):
        current = self.root
        succ = None
        while current:
            if key < current.key:
                succ = current # update successor
                current = current.left
            else:
                current = current.right
        return succ.value if succ else None

# helper function to break text into lowercase words
def getWords(text):
    return text.lower().split()

# Indexes to store individual words and their corresponding sayings
index_span = {} #maps each spanish word to the Saying objects with that word
index_eng = {} #maps each english word to the Saying objects with that word

# adds words from saying to the index for fast word-based lookup
def indexSaying(saying):
    for word in getWords(saying.spanish): # for each word in the sentence
        index_span.setdefault(word, []).append(saying) #map to the list of sayings
    for word in getWords(saying.english):# Same logic for english words

        index_eng.setdefault(word, []).append(saying)

# returns sayings that contain the given spanish word
def MeHua(word):
    return index_span.get(word.lower(), [])

# returns sayings that contain the given english word
def WithWord(word):
    return index_eng.get(word.lower(), [])

#for test cases here is a list of spanish sayings with their english translations
if __name__ == "__main__":
    tree = RBTree()

    sayings = [
        Saying("A buen hambre no hay mal pan", "To a good hunger, there’s no bad bread",
               "Cuando tienes hambre, todo parece bueno.", "When you're hungry, everything tastes good."),
        Saying("Más vale pájaro en mano que ciento volando", "A bird in the hand is worth two in the bush",
               "Es mejor tener algo seguro que arriesgarse por más.", "Better something certain than risky abundance."),
        Saying("El tiempo lo cura todo", "Time heals everything",
               "Con el tiempo, todo dolor disminuye.", "Eventually, all pain fades."),
        Saying("Ojos que no ven, corazón que no siente", "Out of sight, out of mind",
               "Lo que no se ve, no afecta.", "What isn’t seen can’t hurt."),
        Saying("No hay mal que por bien no venga", "Every cloud has a silver lining",
               "Las cosas malas pueden traer cosas buenas.", "Bad things can lead to good outcomes.")
    ]


# test cases
    for s in sayings:
        tree.insert(s.spanish, s)
        indexSaying(s)

    print("Get function:")
    print(tree.get("Ojos que no ven, corazón que no siente"))
    print()

    print("Member function:")
    print("El tiempo lo cura todo:", tree.member("El tiempo lo cura todo"))  # True
    print("Nonexistent phrase:", tree.member("No existe esta frase"))        # False
    print()

    print("First:")
    print(tree.first())
    print()

    print("Last:")
    print(tree.last())
    print()

    print("predecessor:")
    key = "Más vale pájaro en mano que ciento volando"
    print(f"Predecessor of '{key}':")
    print(tree.predecessor(key))
    print()

    print("successor:")
    key = "A buen hambre no hay mal pan"
    print(f"Successor of '{key}':")
    print(tree.successor(key))
    print()

    print("MeHua('cura')")
    for s in MeHua("cura"):
        print(s)
    print()

    print("WithWord('sight'):")
    for s in WithWord("sight"):
        print(s)
    print()
