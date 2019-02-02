import re
import node
from iterator import XMLIterator


class XMLParser:
    tag_reg_patterns = {
        "opening": '<[^0-9/.,:;!?][^\s><]*[^/]>',
        "opening_with_attr": '<[^0-9/.,:;!?][^><]*\s[^><]*[^/]>',
        "closing": '</[^\s]+?>',
        "self_closing": '<[^0-9/.,:;!?][^><]*?/>',
        "service": '(?i)<(\?xml|!--).*?>'
    }

    def __init__(self, buffer):
        self._tag_reg_objects = {key: re.compile(XMLParser.tag_reg_patterns[key])
                                 for key in XMLParser.tag_reg_patterns}
        self._xml_buffer = buffer
        self._xml_buffer_size = len(buffer)
        self._index = 0

        self._root_node = self._parse()

    def get_iterator(self):
        return XMLIterator(self._root_node)

    def _parse(self):
        xml_node = None
        while self._index < self._xml_buffer_size:
            if self._xml_buffer[self._index] == '<':
                tag = self._get_tag(self._xml_buffer[self._index:])

                if self._is_valid_tag(tag):
                    tag_name = self._get_tag_name(tag)
                    tag_attr = self._get_tag_attr(tag)
                    tag_text = self._get_text(self._xml_buffer[self._index:])

                    if self._is_opening_tag(tag):
                        next_tag = self._get_next_tag(self._xml_buffer[self._index:])
                        next_tag_name = self._get_tag_name(next_tag)

                        if self._is_opening_tag(next_tag):
                            xml_node = node.XMLCompositeNode(name=tag_name, attr=tag_attr, text=tag_text)
                            while (not self._is_closing_tag(next_tag)) and (next_tag_name != tag_name):
                                xml_node.add_node(self._parse())

                                # Adding the rest of the tag's text which may be between nested tags
                                rest_tag_text = self._get_text(self._xml_buffer[self._index:])
                                text = xml_node.tag_text + rest_tag_text
                                xml_node.tag_text = text

                                next_tag = self._get_next_tag(self._xml_buffer[self._index:])

                            self._skip_tag(self._xml_buffer[self._index:])
                            return xml_node

                        elif self._is_closing_tag(next_tag) and next_tag_name == tag_name:
                            self._skip_tag(self._xml_buffer[self._index:])

                            return node.XMLLeafNode(name=tag_name, attr=tag_attr, text=tag_text)

                    elif self._is_self_closing_tag(tag):
                        return node.XMLLeafNode(name=tag_name, attr=tag_attr, text=tag_text)

                    continue

                elif self._is_service_tag(tag):
                    continue
                else:
                    raise SyntaxError("The invalid tag - {}".format(tag))

            self._index += 1
        return xml_node

    def _get_tag(self, buff):
        tag = ""
        for char in buff:
            self._index += 1
            tag += char
            if char == '>':
                break
        return tag

    def _get_next_tag(self, buff):
        tag = ""
        index = 0
        size_buff = len(buff)
        while index < size_buff:
            if buff[index] == '<':
                for char in buff[index:]:
                    tag += char
                    if char == '>':
                        break
                break

            index += 1
        return tag

    def _get_tag_name(self, tag):
        return re.search("</?([^<>\s]+).*?>", tag).group(1)

    def _get_tag_attr(self, tag):
        attributes = {}
        attr_search = re.search("<[^<>]*?\s+(.*?)\s*/?>", tag)
        if attr_search:
            attr_string = attr_search.group(1)
            attr_list = re.split('=?\"\s*', attr_string)
            if not attr_list[-1]:
                del attr_list[-1]
            attributes = {attr_list[i]: attr_list[i+1] for i in range(0, len(attr_list), 2)}

        return attributes

    def _get_text(self, buff):
        text = ""
        for char in buff:
            if char == '<':
                break
            self._index += 1
            # Skip whitespace characters
            if char == '\t' or char == '\n':
                continue
            text += char

        if re.search('^\s+$', text):
            text = ""

        return text

    def _skip_tag(self, buff):
        for char in buff:
            self._index += 1
            if char == '>':
                break

    def _is_opening_tag(self, tag):
        result = False
        if self._tag_reg_objects["opening"].search(tag) \
                or self._tag_reg_objects["opening_with_attr"].search(tag):
            result = True

        return result

    def _is_closing_tag(self, tag):
        return self._tag_reg_objects["closing"].search(tag)

    def _is_self_closing_tag(self, tag):
        return self._tag_reg_objects["self_closing"].search(tag)

    def _is_service_tag(self, tag):
        return self._tag_reg_objects["service"].search(tag)

    def _is_valid_tag(self, tag):
        return self._is_opening_tag(tag) or self._is_closing_tag(tag) or self._is_self_closing_tag(tag)
