from __future__ import absolute_import, unicode_literals

import re
from collections import OrderedDict, defaultdict
from xml.etree import ElementTree

from six import text_type
from six.moves.urllib.parse import urlencode


def to_pythonic_name(name):
    """
    Create a Pythonic version of a string.

    *Note: This is an internal API and may be changed without notice.*

    :arg name: string to build a Pythonic version of.

    :rtype: string
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_pythonic_dict(dictionary):
    """
    *Note: This is an internal API and may be changed without notice.*
    """
    # TODO: This should probably be cleaned up, and also support dictionaries
    # in lists
    return {
        to_pythonic_name(k): (
            to_pythonic_dict(v) if isinstance(v, dict) else v)
        for k, v in dictionary.items()
    }


def handle_xml_value(value):
    """
    The AltaPay XML does not contain a scheme, and as such, guesswork has to be
    employed in order to produce decent values.

    This function parses values of the decoded XML, and ensures both digits and
    boolean values.

    *Note: This is an internal API and may be changed without notice.*

    :arg value: value to be parsed (can be a complex datatype)

    :rtype: depends on the input argument
    """
    if not isinstance(value, str) and not isinstance(value, text_type):
        return value

    value = text_type(value)

    if value == 'true':
        return True
    elif value == 'false':
        return False
    elif value.isdigit():
        return int(value)
    elif value.lower() in ('nan', 'inf', '-inf'):
        return value

    try:
        return float(value)
    except ValueError:
        pass

    return value


def xml_to_dict(xml):
    """
    :arg xml: XML document in string representation

    :rtype: :samp:`dict`
    """
    return etree_to_dict(ElementTree.XML(xml.encode('utf-8')))


def etree_to_dict(tree):
    """
    *Note: This is an internal API and may be changed without notice.*
    """
    d = {tree.tag: {} if tree.attrib else None}
    children = list(tree)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(handle_xml_value(v))
        d = {
            tree.tag: {
                k: handle_xml_value(v[0])
                if len(v) == 1 else handle_xml_value(v)
                for k, v in dd.items()
            }
        }
    if tree.attrib:
        d[tree.tag].update(
            ('@' + k, handle_xml_value(v)) for k, v in tree.attrib.items())
    if tree.text:
        text = tree.text.strip()
        if children or tree.attrib:
            if text:
                d[tree.tag]['#text'] = text
        else:
            d[tree.tag] = text
    return d


def http_build_query_dict(payload):
    # Here be dragons
    def unpack_dict(value, key=None):
        if isinstance(value, list):
            for i, elem in enumerate(value):
                yield list(unpack_dict(elem, key='{}[{}]'.format(key, i)))
        elif isinstance(value, dict):
            for k, v in value.items():
                yield list(unpack_dict(v, key='{}[{}]'.format(key, k)))
        else:
            yield key, text_type(value)

    def unpack_list(value, data):
        for elem in value:
            if isinstance(elem, list):
                unpack_list(elem, data)
            else:
                data[elem[0]] = elem[1]

    data = OrderedDict()
    for key, value in payload.items():
        unpack_list(list(unpack_dict(value, key)), data)
    return data


def http_build_query(payload):
    """
    Build a query string that matches the way PHP does it with
    :samp:`http_build_query`.

    In output, this function loosely matches what PHP does in the function
    :samp:`http_build_query`. It handles complex types of both dict and list.

    If :py:class:`collections.OrderedDict` is used, the order of the keys will
    be preserved in the finalized query string.

    *Note: This is an internal API and may be changed without notice.*

    :arg payload: the payload to convert to a query string. This has to be
        :samp:`dict` compatible, but can hold lists as values in the
        dictionary. Nested dictionaries can be used, and lists can hold
        dictionaries.

    :rtype: :samp:`string` that can be used as a GET parameter for HTTP
        requests
    """
    return urlencode(http_build_query_dict(payload))
