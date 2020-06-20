import json

#constants for work with json
CONFIG_FILE_PATH = "words.json"
WORD_LIST_KEY = "words"

class T9:
    def __init__(self):
        self.__words = set()
        self.read_words()

    def read_words(self):
        with open(CONFIG_FILE_PATH) as json_file:
            data = {}
            try:
                data = json.load(json_file)
            except:
                print("Error with reading config file" + CONFIG_FILE_PATH)

            for element in data[WORD_LIST_KEY]:
                try:
                    self.__words.add(element)
                except:
                    print("Error in with word\n")

    def find_node_by_prefix(self, prefix):
        node = self.__root

        for ch in prefix:
            if ch not in node.children_map:
                return None
            else:
                node = node.children_map[ch]
        
        return node

    def find_words(self, prefix):
        node = self.find_node_by_prefix(prefix)
        if node is None:    #no matches
            return []
        end_nodes = self.find_end_nodes(node)
        if node.end_of_word:
            end_nodes.append(node)
        return [self.make_word(n) for n in end_nodes]

    def make_word(self, node):
        word = ""

        while node is not self.__root:
            word = word + node.char
            node = node.parent

        return word[::-1] #reversing

    def find_end_nodes(self, node):
        nodes = []
        if node is None:
            return nodes
        
        for child in node.children:
            if child.end_of_word:
                nodes.append(child)

            nodes = nodes + self.find_end_nodes(child)

        return nodes
            

    def build_trie(self):
        self.__root = Node()

        for word in self.__words:
            node = self.__root

            for ch in word:
                node = node.add_child_if_needed(ch)
            
            node.end_of_word = True

class Node:
    def __init__(self, ch = ""):
        self.char = ch
        self.parent = None
        self.children = []  #nodes
        self.end_of_word = False
        self.children_map = {}

    def add_child_if_needed(self, ch = ""):
        if ch not in self.children_map:
            node = Node(ch)
            node.parent = self
            self.children.append(node)
            self.children_map[ch] = node
            return node
        else:
            return self.children_map[ch]


if __name__ == "__main__":
    t9 = T9()
    t9.build_trie()
    res = t9.find_words("a")
    print(res)
    