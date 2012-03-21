import os
import unittest

from yammy.translator import YammyInputBuffer, yammy_to_html_string, yammy_to_html


class TestYammyTranslator(unittest.TestCase):
    
    def _check(self, yammy, html):
        translated_html = yammy_to_html_string(yammy) 
        self.failUnlessEqual(html, translated_html)

    def _compare_files(self, source, dest):
        with open(source) as f:
            source_content = ''.join([l.strip() for l in f.readlines()])
        with open(dest) as f:
            dest_content = ''.join([l.strip() for l in f.readlines()])
        same = source_content == dest_content
        if not same:
            p = 0
            for c in source_content:
                if c == dest_content[p]:
                    p += 1
                else:
                    break
            print '\nBAD : %s\nGOOD: %s' % (source_content[p-10:p+10], dest_content[p-10:p+10])
        return same

    def _translate_file(self, yammy_file, html_file):
        tmp_html = yammy_file + '.html'
        same = False
        try:
            yammy_to_html(yammy_file, tmp_html)
            same = self._compare_files(tmp_html, html_file)
        finally:
            os.unlink(tmp_html)
        self.failUnless(same, msg='%s translation failed' % yammy_file)

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
            '<div class="settings_main_block"><h5>{{_("Label:")}}</h5><div></div></div>'
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
                    '<div>- some text</div>');

    def test_empty_string(self):
        self._check('', '');

    def test_inline_attributes(self):
        self._check('input[type="submit"]', 
                    '<input type="submit"/>');
        self._check('option[value="10"][selected]', 
                    '<option selected="selected" value="10"></option>');
        self._check('a.class#id[href="/"][id="new_id"] reference', 
                    '<a class="class" href="/" id="new_id">reference</a>');

    def test_files(self):
        module_path = os.sep.join(__name__.split('.')[:-1])
        filenames = tuple(os.walk(module_path))[0][2]
        for filename in filenames:
            if filename[-4:] == '.ymy':
                self._translate_file(
                    os.sep.join([module_path, filename]),
                    os.sep.join([module_path, filename.replace('.ymy', '.html')])
                )


class TestYsammyInputBuffer(unittest.TestCase):
    
    def test_iteration(self):
        for l in YammyInputBuffer(['test']):
            self.assertEqual(l, 'test')