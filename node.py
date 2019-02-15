class XMLNode:
    def __init__(self, **kwargs):
        self._dict_tag_info = kwargs

    @property
    def tag_name(self):
        return self._dict_tag_info['name']

    @property
    def tag_attr(self):
        return self._dict_tag_info['attr']

    @property
    def tag_text(self):
        return self._dict_tag_info['text']

    @tag_text.setter
    def tag_text(self, text):
        self._dict_tag_info['text'] = text

    def get_node_info(self):
        """
        This method must be implemented by subclasses.
        :return: node info as a dictionary of name, attributes and text.
        """
        raise NotImplementedError()


class XMLCompositeNode(XMLNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._xml_node_list = []

    def get_subnode_list(self):
        return self._xml_node_list

    def add_node(self, xml_node):
        self._xml_node_list.append(xml_node)

    def rem_node(self, xml_node):
        self._xml_node_list.remove(xml_node)

    def get_node_info(self):
        info_list = [self._dict_tag_info]
        if self._xml_node_list:
            info_list.append([node.get_node_info() for node in self._xml_node_list])

        return info_list


class XMLLeafNode(XMLNode):
    def get_node_info(self):
        return self._dict_tag_info
