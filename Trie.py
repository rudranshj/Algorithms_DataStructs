class Trie:
    def __init__(self):
        self.trie={} # a dictionary

    def insert(self, word):
        node=self.trie
        for w in word:
            if w not in node: node[w]={}
            node=node[w]
        node['*']=True # to mark the ending of the word: w is also contained
        
    def search(self, word):
        node=self.trie
        for w in word:
            if w not in node: return False
            node=node[w]
        return '*' in node
        
    def startsWith(self, prefix):
        node=self.trie
        for w in prefix:
            if w not in node: return False
            node=node[w]
        return True

