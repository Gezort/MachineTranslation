import sys

from tree import Tree


class Reorderer:
    def reorder(self, root):
        assert False, "Not implemented."

class RecursiveReorderer(Reorderer):
    def reorder(self, tree):
        return self.reorder_recursively(tree.root, [])

    def reorder_recursively(self, head, ordering):
        # 1. Call 'reorder_head_and_children' to determine order of immediate subtree.
        # 2. Walk through immediate subtree in this order, calling 'reorder_recursively'
        # on children and adding head to 'ordering' when it's reached.
        immediate_subtree = self.reorder_head_and_children(head)
        for node in immediate_subtree:
            if node != head:
                ordering.extend(self.reorder_recursively(node, []))
            else:
                ordering.append(head)
        return ordering

    def reorder_head_and_children(self, head):
        # Reorder the head and children in the desired order.
        assert False, "TODO: implement me in a subclass."


class DoNothingReorderer(RecursiveReorderer):
    # Just orders head and child nodes according to their original index.
    def reorder_head_and_children(self, head):
        all_nodes = (
            [(child.index, child) for child in head.children] + [(head.index, head)])
        return [node for _, node in sorted(all_nodes)]


class ReverseReorderer(RecursiveReorderer):
    # Reverse orders head and child nodes according original index
    def reorder_head_and_children(self, head):
        all_nodes = (
            [(child.index, child) for child in head.children] + [(head.index, head)])
        return [node for _, node in sorted(all_nodes, reverse=True)]

class HeadFinalReorderer(RecursiveReorderer):
    def reorder_head_and_children(self, head):
        all_nodes = [(child.index, child) for child in head.children]
        return [node for _, node in sorted(all_nodes)] + [head]

class SOVReorderer(RecursiveReorderer):
    def reorder_head_and_children(self, head):
        all_nodes = head.children + [head]
        if head.tag[:2] == 'VB':
            normal_labels = {'advcl': -1, 'nsubj': 0, 'prep': 0, 'dobj': 1}
            reverse_labels = ['prt', 'aux', 'auxpass', 'neg']
        elif head.tag[:2] == 'JJ':
            normal_labels = {'advcl': -1}
            reverse_labels = ['aux', 'auxpass', 'neg', 'cop']
        elif head.tag[:2] == 'NN':
            normal_labels = {'prep': -2, 'rcmod': -1}
            reverse_labels = []
        else:
            normal_labels = {'pobj': -1}
            reverse_labels = []
        normal = []
        untouched = []
        reverse = []
        for node in all_nodes:
            if node == head:
                reverse += [(head.index, head)]
                continue
            if node.label in normal_labels:
                normal += [(normal_labels[node.label], node.index, node)]
            elif node.label in reverse_labels:
                reverse += [(node.index, node)]
            else:
                untouched += [(node.index, node)]
        res = [node for _, _, node in sorted(normal, key=lambda x: (x[0], x[1]))] + \
              [node for _, node in sorted(untouched)] + \
              [node for _, node in sorted(reverse, reverse=True)]
        return res


if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print "python reorderers.py ReordererClass parses"
        sys.exit(0)
    # Instantiates the reorderer of this class name.
    reorderer = eval(sys.argv[1])()

    # Reorders each input parse tree and prints words to std out.
    for line in open(sys.argv[2]):
        t = Tree(line)
        assert t.root
        reordering = reorderer.reorder(t)
        print ' '.join([node.word for node in reordering if node != t.root])
