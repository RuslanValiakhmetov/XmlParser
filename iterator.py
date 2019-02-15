import node


class XMLIterator:
    def __init__(self, root_node):
        self._root_node = self._parent_node = self._current_node = root_node
        self._parent_stack = []
        self._current_index = 0

    def get_root_node(self):
        self._parent_node = self._current_node = self._root_node
        self._parent_stack = []
        self._current_index = 0

        return self._current_node

    def get_current_node(self):
        return self._current_node

    def get_first_subnode(self):
        if not isinstance(self._current_node, node.XMLCompositeNode):
            return None

        parent_dict_info = {'parent_index': self._current_index, 'parent_object': self._current_node}
        self._parent_stack.append(parent_dict_info)

        self._parent_node = self._current_node
        self._current_index = 0
        self._current_node = self._parent_node.get_subnode_list()[self._current_index]

        return self._current_node

    def get_next_node(self):
        self._current_index += 1
        try:
            self._current_node = self._parent_node.get_subnode_list()[self._current_index]
        except IndexError:
            self._current_index -= 1
            return None

        return self._current_node

    def get_previous_node(self):
        if self._current_index == 0:
            return None

        self._current_index -= 1
        self._current_node = self._parent_node.get_subnode_list()[self._current_index]

        return self._current_node

    def get_parent_node(self):
        if not self._parent_stack:
            return None

        parent_dict_info = self._parent_stack[-1]
        del self._parent_stack[-1]

        self._current_index = parent_dict_info['parent_index']
        self._current_node = parent_dict_info['parent_object']

        if self._parent_stack:
            self._parent_node = self._parent_stack[-1]['parent_object']
        else:
            self._parent_node = self._current_node

        return self._current_node

    def is_root_node(self, in_node):
        return self._root_node == in_node

    def is_parent_node(self):
        return isinstance(self._current_node, node.XMLCompositeNode)
