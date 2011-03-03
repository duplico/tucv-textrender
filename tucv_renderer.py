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
        space_col = ' ' * sep
        left_width = 80 - RIGHT_COLUMN_WIDTH - sep - indent
        print 'printing l', type(left), 'r', type(right)
        i_indent = ' ' * indent
        if indent == 0:
            i_indent = 'o '
            indent = 2
        left_col = textwrap.wrap(left,
                                 width=left_width, initial_indent=i_indent,
                                 subsequent_indent=' '*indent)
        right_col = textwrap.wrap(right,
                                  width=RIGHT_COLUMN_WIDTH)
        if len(left_col) < len(right_col):
            left_col += [''] * (len(right_col)-len(left_col))
        if len(left_col) > len(right_col):
            right_col += [''] * (len(left_col)-len(right_col))
        print left_col, right_col
        lines = map(lambda l,r: ''.join([l, space_col,  ' '*(sep+left_width-len(l)), r]),
            left_col, right_col)
        return '\n'.join(lines) + '\n'
    
    def text_entry_one_col(self, left, indent=0):
        left_width = 80 - RIGHT_COLUMN_WIDTH - indent
        left_col = textwrap.wrap(textwrap.dedent(left).strip(),
                                 width=left_width, initial_indent=' '*indent,
                                 subsequent_indent=' '*indent)
        return '\n'.join(left_col) + '\n'
    
    def resheading(self, node):
        return '\n' + node.attributes['heading'].upper() + '\n'
    
    def resentry(self, node):
        left = unicode(node.attributes['left'])
        right = unicode(node.attributes['right'])
        spacing = 0
        if node.attributes['indent']:
            spacing = 2
        return self.text_entry_two_col(left, right,
                                       indent=0)
    
    def ressubentry(self, node):
        return self.text_entry_two_col(unicode(node.attributes['lefttext']),
                                       unicode(node.attributes['righttext']),
                                       indent=1)
        
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

    def resschool(self, node):
        school_string = unicode(node.attributes['name'])
        rendered_school_string = self.text_entry_two_col(school_string,
                                       unicode(node.attributes['location']),
                                       indent=0)
        if 'description' in node.attributes and node.attributes['description']:
            rendered_school_string += self.text_entry_one_col(unicode(node.attributes['description']), indent=3)
        return rendered_school_string
    
    def resdegree(self, node):
        left_side = unicode(node.attributes['degree']) + ' in ' + \
            unicode(node.attributes['major'])
        print 'here'
        print left_side
        print 'and', unicode(node.attributes['date'])
        rendered_text = self.text_entry_two_col(left_side,
                                       unicode(node.attributes['date']),
                                       indent=3)
        if 'description' in node.attributes and node.attributes['description']:
            rendered_text += self.text_entry_one_col(unicode(node.attributes['description']), indent=4)
        return rendered_text
        pass # Date major description degree
    
    def resemployer(self, node):
        left_side = unicode(node.attributes['name'])
        rendered_text = self.text_entry_two_col(left_side,
                                       unicode(node.attributes['location']),
                                       indent=0)
        if 'description' in node.attributes and node.attributes['description']:
            rendered_text += self.text_entry_one_col(unicode(node.attributes['description']), indent=3)
        return rendered_text
        pass # description name location
    
    def resjob(self, node):
        left_side = unicode(node.attributes['title'])
        
        rendered_text = self.text_entry_two_col(left_side,
                                       unicode(node.attributes['startdate']) + ' -\n' +\
                                       unicode(node.attributes['enddate']),
                                       indent=1)
        if 'description' in node.attributes and node.attributes['description']:
            rendered_text += self.text_entry_one_col(unicode(node.attributes['description']), indent=3)
        return rendered_text
        pass # startdate enddate description title
    
    def resdesc(self, node):
        text = unicode(node.attributes['item']) + ' - ' + \
               unicode(node.attributes['description'])
        rendered_text = textwrap.wrap(textwrap.dedent(text).strip(),
                                 width=60, initial_indent='o ',
                                 subsequent_indent='   ')
        print rendered_text
        return u'\n'.join(rendered_text) + '\n'
        pass # item description
    
    def resconference(self, node):
        pass # role description name
    
    def ressubconference(self, node):
        pass # role description name
    
    def resbib(self, node):
        pass # title
    
    def default(self, node):
        """ Rendering method for all non-text nodes """
        s = []

        # Handle characters like \&, \$, \%, etc.
        if len(node.nodeName) == 1 and node.nodeName not in string.letters:
            return self.textDefault(node.nodeName)
        
        supported = ['resheading', 'resentry', 'ressubentry',
                     'resentrysinglecol', 'ressubentrysinglecol',
                     'resschool', 'resdegree', 'resemployer',
                     'resjob', 'resdesc','resconference', 'ressubconference', 
                     'resbib']
        supported = supported[:10]
        if node.nodeName in supported:
            print 'Supported node', node.nodeName
            s.append(getattr(self, node.nodeName)(node))
        else:
            
            print 'Unsupported node', node.nodeName
            # Start tag
            #s.append('<%s>' % node.nodeName)
    
            # See if we have any attributes to render
            
            #if node.hasAttributes():
            #    s.append('<attributes>')
            #    for key, value in node.attributes.items():
            #        # If the key is 'self', don't render it
            #        # these nodes are the same as the child nodes
            #        if key == 'self':
            #            continue
            #        s.append('<%s>%s</%s>' % (key, unicode(value), key))
            #    s.append('</attributes>')
    
            # Invoke rendering on child nodes
            s.append(unicode(node))
    
            # End tag
            #s.append('</%s>' % node.nodeName)

        return u'\n'.join(s)

    def textDefault(self, node):
        """ Rendering method for all text nodes """
        return node.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').strip()
        
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

if __name__ == '__main__':
    render('my-resume.tex')