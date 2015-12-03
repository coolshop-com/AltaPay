from __future__ import absolute_import, unicode_literals

import re
from collections import defaultdict


def to_pythonic_name(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def etree_to_dict(tree):
    d = {tree.tag: {} if tree.attrib else None}
    children = list(tree)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {
            tree.tag: {
                k: v[0] if len(v) == 1 else v for k, v in dd.items()
            }
        }
    if tree.attrib:
        d[tree.tag].update(('@' + k, v) for k, v in tree.attrib.items())
    if tree.text:
        text = tree.text.strip()
        if children or tree.attrib:
            if text:
                d[tree.tag]['#text'] = text
        else:
            d[tree.tag] = text
    return d
