import os
import unittest

from yammy.translator import YammyInputBuffer, \
                             yammy_to_html_string, yammy_to_html


class TestYammyTranslator(unittest.TestCase):

    def _check(self, yammy, html):
        translated_html = yammy_to_html_string(yammy)
        self.failUnlessEqual(html, translated_html)

    def _compare_files(self, source, dest, ignore_spaces=False):
        with open(source) as f:
            source_content = ''.join([l.strip() for l in f.readlines()])
        with open(dest) as f:
            dest_content = ''.join([l.strip() for l in f.readlines()])
        if ignore_spaces:
            source_content = source_content.replace(' ', '')
            dest_content = dest_content.replace(' ', '')
        same = source_content == dest_content
        if not same:
            p = 0
            for c in source_content:
                if c == dest_content[p]:
                    p += 1
                else:
                    break
            print '\nBAD : %s\nGOOD: %s' % (source_content[p - 10:p + 10],
                                            dest_content[p - 10:p + 10])
        return same

    def _do_translate_file(self, yammy_file, html_file,
                           keep_line_numbers=False):
        tmp_html = yammy_file + '.html'
        same = False
        try:
            yammy_to_html(yammy_file,
                          tmp_html,
                          keep_line_numbers=keep_line_numbers)
            same = self._compare_files(tmp_html, html_file,
                                       ignore_spaces=keep_line_numbers)
        finally:
            os.unlink(tmp_html)
        self.failUnless(same, msg='%s translation failed' % yammy_file)

    def _translate_file(self, yammy_file, html_file):
        self._do_translate_file(yammy_file, html_file, keep_line_numbers=False)
        self._do_translate_file(yammy_file, html_file, keep_line_numbers=True)

    def test_css_class_id(self):
        self._check(
            'div.class#id some text',
            '<div class="class" id="id">some text</div>'
        )

    def test_css_class_id_no_text(self):
        self._check(
            'div.class#id',
            '<div class="class" id="id"></div>'
        )

    def test_idents(self):
        self._check(
            '''
            div.settings_main_block
                        h5
                            | {{_("Label:")}}
\t                    div
            ''',
            '<div class="settings_main_block">'
            '<h5>{{_("Label:")}}</h5><div></div></div>'
        )

    def test_inner_text(self):
        self._check('''
div
    - class class
    - id id
   | some text
   | and next text line
''',
            '<div class="class" id="id">some text and next text line</div>'
        )

    def test_escape(self):
        self._check("div\n" +
                    "    \- some text",
                    '<div>- some text</div>')

    def test_empty_string(self):
        self._check('', '')

    def test_inline_attributes(self):
        self._check('input[type="submit"]',
                    '<input type="submit"/>')
        self._check('input[type=submit]',
                    '<input type="submit"/>')
        self._check('input[type=submit]',
                    '<input type="submit"/>')
        self._check('option[value="10"][selected]',
                    '<option selected="selected" value="10"></option>')
        self._check('a.class#id[href="/"][id="new_id"] reference',
                    '<a class="class" href="/" id="new_id">reference</a>')
        self._check('a.class#id[href=/][id=new_id] reference',
                    '<a class="class" href="/" id="new_id">reference</a>')

    def test_files(self):
        module_path = os.sep.join(__name__.split('.')[:-1])
        filenames = tuple(os.walk(module_path))[0][2]
        for filename in filenames:
            if filename[-4:] == '.ymy':
                self._translate_file(
                    os.sep.join([module_path, filename]),
                    os.sep.join([module_path,
                                 filename.replace('.ymy', '.html')])
                )

    def test_on_off(self):
        self._check(
            '''
!PLAIN
lorem and ipsum
ipsum and lorem
!YAMMY
            div.clear
!HTML
<p>
    lorem and ipsum
    ipsum and lorem
</p>
!YAMMY
            div.clear
!TEXT
some really meaningless text
!YAMMY
            div.clear
            ''',
            '''lorem and ipsum
ipsum and lorem
<div class="clear"></div><p>
    lorem and ipsum
    ipsum and lorem
</p>
<div class="clear"></div>some really meaningless text
<div class="clear"></div>''')

    def test_on_and_off2(self):
        self._check('''
html
    body
        !HTML
        <p>
            Hi!
        </p>''',
        '''<html><body>        <p>
            Hi!
        </p>
</body></html>''')

    def test_debug_mode(self):
        source_string = '''<div>test</div>
div.wrapper
    div My content goes here'''
        html = '''<div>test</div>
<div class="wrapper"
><div>My content goes here</div></div>'''

        translated_html = yammy_to_html_string(source_string,
                                               keep_line_numbers=True)
        self.failUnlessEqual(html, translated_html)


class TestYammyInputBuffer(unittest.TestCase):

    def test_iteration(self):
        for l in YammyInputBuffer(['test']):
            self.assertEqual(l, 'test')
