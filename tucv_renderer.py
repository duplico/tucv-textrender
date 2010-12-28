import string
import re
import textwrap
from plasTeX.Renderers import Renderer
from plasTeX.TeX import TeX

import tucv

RIGHT_COLUMN_WIDTH = 15
COLUMN_SEP = 5

class Renderer(Renderer):
    
    def text_entry_two_col(self, left, right, sep=COLUMN_SEP, indent=0):
        text = ''
        space_col = ' ' * sep
        left_width = 80 - RIGHT_COLUMN_WIDTH - sep - indent
        left_col = textwrap.wrap(textwrap.dedent(left).strip(),
                                 width=left_width, initial_indent=' '*indent,
                                 subsequent_indent=' '*indent)
        right_col = textwrap.wrap(textwrap.dedent(right).strip(),
                                  width=RIGHT_COLUMN_WIDTH)
        lines = map(lambda l,r: ''.join([space_col, l, ' '*sep, r]),
            left_col, right_col)
        return '\n'.join(lines)
    
    def resentry(self, node):
        left = node.attributes('lefttext')
        right = node.attributes('righttext')
        spacing = 0
        if node.attributes('indent'):
            spacing = 2
        return self.text_entry_two_col(left, right,
                                       indent=spacing)
    
    def ressubentry(self, node):
        return self.text_entry_two_col(unicode(node.attributes['lefttext']),
                                       unicode(node.attributes['righttext']))
        
    def resentrysinglecol(self, node, space=None):
        left = node.attributes['text']
        space = False
        space_col = ''
        if space:
            space_col = ' '
        lines = textwrap.fill(unicode(left), width=60, initial_indent=space_col,
                              subsequent_indent=space_col)
        return lines
    
    def ressubentrysinglecol(self, left):
        return self.resentrysinglecol(left, space=1)
    
    def resheading(self, node):
        return node.attributes['heading'].upper()

    def resschool(self, node):
        school_string = unicode(node.attributes['name'])
        if node.attributes['description']:
            school_string = '\n'.join((school_string,
                                       unicode(node.attributes['description'])))
        return self.text_entry_two_col(school_string,
                                       unicode(node.attributes['location']),
                                       indent=1)
    
    def default(self, node):
        """ Rendering method for all non-text nodes """
        s = []

        # Handle characters like \&, \$, \%, etc.
        if len(node.nodeName) == 1 and node.nodeName not in string.letters:
            return self.textDefault(node.nodeName)
        
        supported = ['resheading', 'resentry', 'ressubentry',
                     'resentrysinglecol', 'ressubentrysinglecol',
                     'resschool', 'resdegree', 'resemployer',
                     'resjob', 'resconference', 'ressubconference', 'resdesc',
                     'resbib']
        supported = supported[:6]
        if node.nodeName in supported:
            print 'Supported node', node.nodeName
            s.append(getattr(self, node.nodeName)(node))
        else:
            print 'Unsupported node', node.nodeName
            # Start tag
            s.append('<%s>' % node.nodeName)
    
            # See if we have any attributes to render
            if node.hasAttributes():
                s.append('<attributes>')
                for key, value in node.attributes.items():
                    # If the key is 'self', don't render it
                    # these nodes are the same as the child nodes
                    if key == 'self':
                        continue
                    s.append('<%s>%s</%s>' % (key, unicode(value), key))
                s.append('</attributes>')
    
            # Invoke rendering on child nodes
            s.append(unicode(node))
    
            # End tag
            s.append('</%s>' % node.nodeName)

        return u'\n'.join(s)

    def textDefault(self, node):
        """ Rendering method for all text nodes """
        return node.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def render(path):
    # Instantiate a TeX processor and parse the input text
    tex = TeX()
    tex.ownerDocument.config['files']['split-level'] = -100
    tex.ownerDocument.config['files']['filename'] = 'test.xml'
    f=open(path)
    tex.input(f)
    document = tex.parse()
    context = document.context
    # Render the document
    renderer = Renderer()
    renderer.render(document)
    f.close()
    return document