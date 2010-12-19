import string
import re
import textwrap
from plasTeX.Renderers import Renderer
from plasTeX.TeX import TeX
from plasTeX import Command, Environment

RIGHT_COLUMN_WIDTH = 15
COLUMN_SEP = 5

class resheading(Command):
    args = 'heading'

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
    
    def resentry(self, left, right, space=None):
        spacing = 0
        if space:
            spacing = 2
        return self.text_entry_two_col(unicode(left), unicode(right),
                                       indent=spacing)
        #text = ''
        #space_col = ''
        #if space:
        #    space_col = ' '
        #left_width = 80 - RIGHT_COLUMN_WIDTH - COLUMN_SEP - len(space_col)
        #left_col = textwrap.wrap(textwrap.dedent(unicode(left)).strip(),
        #                         width=left_width)
        #right_col = textwrap.wrap(textwrap.dedent(unicode(right)).strip(),
        #                          width=RIGHT_COLUMN_WIDTH)
        #lines = map(lambda l,r: ''.join([space_col, l, ' '*COLUMN_SEP, r]),
        #    left_col, right_col)
        #return '\n'.join(lines)
    
    def ressubentry(self, left, right):
        return self.resentry(left, right, 1)
        
    def resentrysinglecol(self, left, space=None):
        text = ''
        space_col = ''
        if space:
            space_col = ' '
        lines = textwrap.fill(unicode(left), width=60, initial_indent=space_col,
                              subsequent_indent=space_col)
        return lines
    
    def ressubentrysinglecol(self, left):
        return self.resentrysinglecol(left, space=1)
    
    def resheading(self, heading):
        return unicode(heading).upper()
    
    def resschool(self, school, location, description=None):
        school_string = unicode(school)
        if description:
            school_string = '\n'.join((school_string,
                                       unicode(description)))
        return self.text_entry_two_col(school_string,unicode(location),indent=1)
    
    def default(self, node):
        """ Rendering method for all non-text nodes """
        print 'Rendering',node.nodeName
        s = []
        supported = ['resentry', 'ressubentry',
                     'resentrysinglecol', 'ressubentrysinglecol',
                     'resschool', 'resdegree', 'resemployer',
                     'resjob', 'resconference', 'ressubconference', 'resdesc',
                     'resbib']
        supported = supported[:0]
        
        # Handle characters like \&, \$, \%, etc.
        if len(node.nodeName) == 1 and node.nodeName not in string.letters:
            return self.textDefault(node.nodeName)

        # Start tag
        s.append('<%s>' % node.nodeName)

        s.append(unicode(node))
        
        #curr_node = node
        #if node.nodeName in supported:
        #    print node.nodeName, 'is supported by tucv.'
        #    # Build a list of parameters
        #    macro_params = []
        #    param = node.nextSibling
        #    print 'Checking parameters / siblings.'
        #    print 'Parent is', node.parentNode.nodeName, node.parentNode.source
        #    print 'Parent children are', map(lambda a: a.nodeName, node.parentNode.childNodes)
        #    while param and (param.nodeName == 'bgroup' or \
        #                     re.match(r'\[.*\]$', param.nodeValue)):
        #        macro_params += [param]
        #        param = param.nextSibling
        #    print 'Parameter/siblings:', map(lambda a: a.source, macro_params)
        #    # Move optional parameter to end.
        #    if macro_params[0].nodeName=='#text':
        #        macro_params = macro_params[1:] + [macro_params[0]]
        #    print 'Calling',node.nodeName,'with',macro_params
        #    return getattr(self, node.nodeName)(*macro_params)

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
    # Render the document
    renderer = Renderer()
    renderer.render(document)
    f.close()
    return document