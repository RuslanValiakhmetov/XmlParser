import os
from sys import exit, argv
from xml_parser import XMLParser


class Main:
    FOUR_SPACES = 4 * ' '

    @staticmethod
    def print_xml_tree(xml_iterator, sub_line):
        if xml_iterator.is_root_node(xml_iterator.get_current_node()):
            print(xml_iterator.get_root_node().tag_name)

        line = sub_line + '|__'
        node = xml_iterator.get_first_subnode()
        while node:
            print(line + node.tag_name)
            if xml_iterator.is_parent_node():
                Main.print_xml_tree(xml_iterator, sub_line + Main.FOUR_SPACES)

            node = xml_iterator.get_next_node()

        # this for returning to parent node after recurse end
        xml_iterator.get_parent_node()

    @staticmethod
    def main(arg):
        try:
            if len(arg) != 1:
                print("Must be only one parameter - path to xml-file.")
                return 1

            xml_file = arg[0]
            if not os.path.isfile(xml_file):
                print("Invalid file - {}.".format(xml_file))
                return 1

            with open(xml_file, 'r') as f:
                buffer = f.read()

            Main.print_xml_tree(XMLParser(buffer).get_iterator(), Main.FOUR_SPACES)

        except Exception as exp:
            print("An error occurred: " + str(exp))
            return -1


if __name__ == "__main__":
    exit(Main.main(argv[1:]))
