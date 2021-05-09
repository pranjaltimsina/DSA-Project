# TRIE DATA STRUCTURE
import os


# Each node of the Trie
class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = True
        self.children = {}


# The Trie itself, in all its glory
class Trie(object):
    # Initialise with a root node
    def __init__(self):
        self.root = TrieNode("")

    # Insert a node to the trie
    def insert(self, word):
        node = self.root
        for char in word.split('/'):
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode('/' + char)
                node.children[char] = new_node
                node = new_node

    # Depth First Search
    def dfs(self, node, pre):
        if node.is_end:
            self.output.append((pre + node.char))
        for child in node.children.values():
            self.dfs(child, pre + node.char)

    # Algorithm to searching for a node and its children
    def search(self, x):
        node = self.root
        for char in x.split('/'):
            if char in node.children:
                node = node.children[char]
            else:
                return []

        self.output = []
        self.dfs(node, '/'.join(x.split('/')[:-1]))
        return self.output


# Return list of files and subdirectories after recursively traversing through
def get_list_of_files(dir_name):
    list_of_file = os.listdir(dir_name)
    all_files = list()
    # Iterate over all them entries
    for entry in list_of_file:
        # Create full path to the entry
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory, get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)
    return all_files

    # Snek Magik
    # list_of_files = list()
    # for (dirpath, dirnames, filenames) in os.walk(dir_name):
    #     list_of_files += [os.path.join(dirpath, file) for file in filenames]
    # return list_of_files


def init_trie(tr, path):
    files = get_list_of_files(path)
    for file in files:
        tr.insert(file)


def main():
    tr = Trie()
    # dir_path = input("Enter your directory path: ")
    dir_path = "/home/krish/Pictures"
    init_trie(tr, dir_path)

    # Gives ALL the results as the tree is traversed in entirety
    print(tr.search("/home"))


if __name__ == '__main__':
    main()
