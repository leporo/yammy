import weakref
from string import ascii_letters, digits


UNARY_HTML_TAGS = set('area,base,basefont,br,col,frame,hr,img,input,isindex,link,meta,param,embed'.split(','))
SCRIPT_HTML_TAGS = ('script', 'style')

TAB_WIDTH = 4 # Replace tab characters with 4 space characters


class TranslatorError(Exception):
    pass


class YammyInputBuffer(object):
    
    def __init__(self, input_lines):
        self.input = iter(input_lines)
        self._current_line = None
        self.indentation = 0
        self.line_number = 0

    def __iter__(self):
        return self

    def next(self):
        while True:
            try:
                line = self.input.next()
                self.line_number += 1
            except StopIteration:
                self._current_line = ''
                raise
            l = line.strip()
            # Skip empty and comment lines
            if(l and l[0] != '#'):
                # replace leading tabs with spaces
                p = 0
                while (p < len(line)):
                    c = line[p]
                    if c == '\t':
                        tab_width = ((p + TAB_WIDTH) / TAB_WIDTH) * TAB_WIDTH - p
                        line = line[:p] + ' ' * tab_width + line[p+1:]
                        p += tab_width
                    elif c == ' ':
                        p += 1
                    else:
                        break
                break
        self.indentation = line.find(l)
        self._current_line = l 
        return self._current_line

    @property
    def line(self):
        if self._current_line is None:
            try:
                self.next()
            except StopIteration:
                self._current_line = ''
        return self._current_line
        

class YammyOutputBuffer(object):
    
    def __init__(self):
        self.current_line = ''

    def __del__(self):
        self.flush()

    def write(self, line):
        self.current_line += line

    def flush(self):
        pass


class YammyOutputFile(YammyOutputBuffer):
    
    def __init__(self, filename):
        super(YammyOutputFile, self).__init__()
        self.file = open(filename, 'w')

    def __del__(self):
        self.flush()
        self.file.close()

    def flush(self):
        if(self.current_line):
            self.file.write(self.current_line)
            self.current_line = ''


class YammyBlockTranslator(object):
    inner_line_types = ()
    
    def __init__(self, input_stream, output_stream, parent=None):
        self.input = input_stream
        self.output = output_stream
        self.indentation = input_stream.indentation
        if parent:
            self.parent_block = weakref.proxy(parent)
        else:
            self.parent_block = None

    def move_to_next_line(self):
        res = True 
        try:
            self.input.next()
        except StopIteration:
            res = False
        return res

#    def translate(self, context=None):
#        self.output.write(self.input.line)
#        self.move_to_next_line()

    def translate_inner_lines(self):
        context = {}
        while self.input.line:
            # Translate nested lines 
            indentation = self.input.indentation
            if indentation > self.indentation:
                self.translate_inner_line(context=context)
            else:
                break

    def translate_inner_line(self, context=None):
        first_line_char = self.input.line[0]
        line_translator = None
        for line_type in self.inner_line_types:
            first_char = line_type[0] 
            if not first_char or (first_line_char in first_char):
                line_translator = line_type[1]
                break
        if line_translator:
            line_translator(self.input, self.output, parent=self).translate(context=context)
        else:
            l = self.input.line
            if l[0] == '\\':
                l = l[1:]  
            self.output.write(l)
            self.move_to_next_line()

    def get_line_part(self, line, delimiters=' ', allow_quotes=False, allowed_chars=None):
        '''
        Returns (part, line_remainder)
        '''
        result = ''
        n_position = 0
        if line:
            if not delimiters:
                result = line
                n_position = len(line)
            elif allow_quotes and line[0] == '"':
                result = line[1:].split('"')[0]
                n_position = len(result) + 2
            else:
                for c in line:
                    if c in delimiters or (allowed_chars and c not in allowed_chars):
                        break
                    else:
                        n_position += 1
                result = line[:n_position]
        return (result.strip(), line[n_position:].strip())


class YammyHTMLAttribute(YammyBlockTranslator):

    def translate(self, context=None):
        line = self.input.line[1:].strip()
        (attribute_name, line) = self.get_line_part(line, delimiters=' ', allow_quotes=False, allowed_chars=ascii_letters + digits + '_-:')
        (attribute_value, line) = self.get_line_part(line, delimiters='', allow_quotes=False)

        if attribute_name:
            self.output.write(' %s="%s' % (attribute_name, attribute_value))
        else:
            self.output.write(' %s' % attribute_value)
        
        self.move_to_next_line()
        self.translate_inner_lines()

        if attribute_name:
            self.output.write('"')


class YammyHTMLInnerText(YammyBlockTranslator):

    def translate(self, context=None):
        if self.parent_block and isinstance(self.parent_block, YammyHTMLTag):
            self.parent_block.close_start_tag()
        if (context is None) or context.get('text_line_no', 0): 
            self.output.write(' ')
        if isinstance(context, dict):
            context['text_line_no'] = context.get('text_line_no', 0) + 1
        self.output.write(self.input.line[1:].strip())

        self.move_to_next_line()


class YammyHTMLInnerExpression(YammyBlockTranslator):

    def translate(self, context=None):
        if self.parent_block and isinstance(self.parent_block, YammyHTMLTag):
            self.parent_block.close_start_tag()
        if (context is None) or context.get('text_line_no', 0): 
            self.output.write(' ')
        if isinstance(context, dict):
            context['text_line_no'] = context.get('text_line_no', 0) + 1
        self.output.write(self.input.line.strip())

        self.move_to_next_line()


class YammyHTMLScript(YammyBlockTranslator):

    def translate(self, context=None):
        if self.parent_block and isinstance(self.parent_block, YammyHTMLTag):
            self.parent_block.close_start_tag()
        if (context is None) or context.get('text_line_no', 0): 
            self.output.write('\n')
        if isinstance(context, dict):
            context['text_line_no'] = context.get('text_line_no', 0) + 1
        self.output.write(self.input.line.strip())

        self.move_to_next_line()


class YammyHTMLTag(YammyBlockTranslator):

    def translate(self, context=None):
        self.tag = ''
        self.start_tag_closed = False
        if self.parent_block and isinstance(self.parent_block, YammyHTMLTag):
            self.parent_block.close_start_tag()
        tag = ''
        tag_attributes = {}
        tag_text = ''
        
        line = self.input.line
        while line:
            c = line[0]
            if c == '.':
                (tag_attributes['class'], line) = self.get_line_part(line[1:], delimiters=' #[', allow_quotes=True)
            elif c == '#':
                (tag_attributes['id'], line) = self.get_line_part(line[1:], delimiters=' .[', allow_quotes=False)
            elif c == '[':
                (attr_name, line) = self.get_line_part(line[1:], delimiters='=]', allow_quotes=False)
                if line and (line[0] != '='):
                    attr_value = attr_name
                else:
                    (attr_value, line) = self.get_line_part(line[1:], delimiters=' ]', allow_quotes=True)
                tag_attributes[attr_name] = attr_value
                # Skip the closing square bracket
                line = line[1:]
            elif tag or tag_attributes:
                (tag_text, line) = self.get_line_part(line, delimiters='', allow_quotes=False)
            else:
                (tag, line) = self.get_line_part(line, delimiters=' .#[', allow_quotes=False)
        
        self.tag = tag.lower()

        if self.tag in SCRIPT_HTML_TAGS:
            self.output.write('\n')
            self.inner_line_types = (
                ('-', YammyHTMLAttribute),
                ('', YammyHTMLScript),
            )
        else:
            self.inner_line_types = (
                ('-', YammyHTMLAttribute),
                ('|\\', YammyHTMLInnerText),
                (ascii_letters, YammyHTMLTag),
                (None, YammyHTMLInnerExpression),
            )

        self.output.write('<%s' % self.tag)
        for attr in sorted(tag_attributes.keys()):
            value = tag_attributes[attr]
            self.output.write(' %s="%s"' % (attr, value))
        self.inner_text = tag_text

        self.move_to_next_line()
        self.translate_inner_lines()

        self.write_end_tag()
        if self.tag in SCRIPT_HTML_TAGS:
            self.output.write('\n')

    def close_start_tag(self):
        if not self.start_tag_closed:
            if self.tag in UNARY_HTML_TAGS:
                self.output.write('/>')
            else:
                self.output.write('>%s' % self.inner_text)
            self.start_tag_closed = True

    def write_end_tag(self): 
        self.close_start_tag()
        if self.tag not in UNARY_HTML_TAGS:
            self.output.write('</%s>' % self.tag)


class YammyTranslator(YammyBlockTranslator):
    inner_line_types = (
        (ascii_letters, YammyHTMLTag),
    )

    def translate(self, context=None):
        self.indentation = -1;
        self.translate_inner_lines()


def yammy_to_html_string(in_string):
    _input = YammyInputBuffer(in_string.split('\n'))
    output = YammyOutputBuffer()
    YammyTranslator(_input, output).translate()
    return output.current_line


def yammy_to_html(in_file_name, out_file_name):
    in_file = open(in_file_name, 'r')
    try:
        _input = YammyInputBuffer(in_file)
        output = YammyOutputFile(out_file_name)
        YammyTranslator(_input, output).translate()
    finally:
        in_file.close()
    return output.current_line
