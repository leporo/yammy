Yammy: A better way to create a Django/Jinja template
=====================================================

Yammy is not a template engine. The Yammy's translator does not handle expressions or condition blocks.
Yammy strips unnecessary parts from HTML template and makes the template collaboration-friendly.

So you may use Yammy Translator as preprocessor with your favorite template engine.

Installation
------------

Yammy is available as PyPI package, so the easiest way to install Yammy is
to use **pip** or **easy_install** Python package manager:

    $ pip install yammy

You may also clone Mercurial repository: 

	$ hg clone https://quasinerd@bitbucket.org/quasinerd/yammy

and manually add the **yammy** package to your project.


Basic Usage
-----------

Yammy Template → Django/Jinja HTML Template → Web Page

    >>> from yammy import yammy_to_html
    >>> yammy_to_html('template.yammy', 'template.html')
    
    >>> from yammy import yammy_to_html_string
    >>> yammy_to_html_string('div\n    | Inner text')

Django Integration
------------------

Configure Django to use template loaders provided by **yammy.django_loaders**
module using the TEMPLATE_LOADERS option in your settings.py:

    TEMPLATE_LOADERS = (
        'yammy.django_loaders.YammyFileSystemLoader',
        'yammy.django_loaders.YammyPackageLoader',
    )


Jinja2 Integration
------------------

Yammy comes with the Jinja2 integration module.
The simplest way to enable a Yammy template processing in your application looks roughly like this:

    from jinja2 import Environment
    from yammy.jinja2_loaders import YammyPackageLoader
    env = Environment(loader=YammyPackageLoader('yourapplication', 'templates'))

Make sure you use .ymy or .yammy extension for your Yammy template files. 
Note you can also mix Yammy templates with HTML ones.  


Jingo Integration
-----------------

Jingo (http://pypi.python.org/pypi/jingo) is an adapter for using Jinja2
templates within Django.

The simpliest way to attach Yammy templates to Jingo adapter is by using a
**yammy.jingo_loaders** module.  

Change the TEMPLATE_LOADERS setting in your settings.py as follows:

    TEMPLATE_LOADERS = (
        'yammy.jingo_loader.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

This code also integrates Jingo/Jinga2 to your Django project.


Command-Line Utility
--------------------

You may use the **yammy** command-line utility for the batch processing of
Yammy templates:

	yammy <source file or folder> [--dest=<destination file or folder name>]


Syntax
======

The Yammy template syntax has much in common with the HAML, Slim and many other similar template engine languages.

Line meaning is being recognized by the first line's character:

 * Lines starting with Latin letters are HTML tags.
 * Lines starting with the '-' character are HTML tag attributes.
 * Lines starting with the '|' (pipe character) define the HTML code and the text that occurs between that element's opening and closing tag.
 * Lines starting with the '#' character are comments.
 * Lines starting with the '!' character are multiline escaping switchers.

Empty lines and trailing spaces are ignored.

You may also use CSS-like selectors to define tag's attributes.

### HTML Tags

    Yammy                     Translates to
    ------------------------- -----------------------------------------------------------
    div Some Text             <div>Some text</div>
    
    div                       <div>Some text</div>
        | Some text

    div.class#id Inner Text   <div class="class" id="id">Inner Text</div>

    div                       <div class="class" id="id">Inner Text</div>
        - class class
        - id id
        | Inner Text
    
    div.class1.class2#id      <div class="class1 class2" id="id">Inner Text</div>
    
    input[type="submit"]      <input type="submit"/>

    input[type=submit]        <input type="submit"/>

### Nesting

Tag nesting is being declared using indentation:

    Yammy                     Translates to
    ------------------------- -----------------------------------------------------------
    div.outer                 <div class="outer"><div class="inner">Some text</div></div>
        div.inner
            | Some text

### Template Engine Statements and Plain HTML

    Yammy                     Translates to
    ------------------------- -----------------------------------------------------------
    <!doctype html>           <!doctype html><html><body></body></html>
    html
        body
    
    {% if target.hit %}       {% if target.hit %}<div class="hit">Hit!</div>{% endif %}
        div.hit Hit!
    {% endif %}

### Multiline escaping

    Yammy                     Translates to
    ------------------------- -----------------------------------------------------------
    html                      <html><body><div>            <p>Hi!</p>
        body                  <p>                How are you?
            div                               Good!
                !HTML         </p></div></body></html>
                <p>Hi!</p>
                !YAMMY
                p
                    !TEXT
                    How are you?
                    !PLAIN
                    Good!

### Scripts and Styles

    Yammy                           Translates to
    ------------------------------- -----------------------------------------------------
    script                          <script>
        $(function(){               $(function(){
            $('.button').click(     $('.button').click(
                function(e){        function(e){
                   console.log(e);  console.log(e);
                }                   }
            );                      );
        });                         });
                                    </script>

### Comments

Yammy does not support multiline comments.
To add a single-line comment start it with the '#' character: 

    Yammy                           HTML
    ------------------------------- -----------------------------------------------------
    div                             <div class="class" id="id">Inner Text</div>
        # let's define a class
        - class class
        # let's specify the id
        - id id
        # let's add the inner text
        | Inner Text

Advantages
==========

### Readability

There are no extra brackets and quotes. Block nesting is defined by their indentation.

### Better collaboration

It's hard to work on the same HTML template with someone else: changes made to long lines with
many attribute definitions are difficult to merge, nested single row condition statements are
difficult to understand and maintain.

With Yammy you may split your template to as many lines as you wish and indent nested blocks.

So it's much easier to figure out what has been changed:

#### HTML template diff

    - <div class="row{% if needs_more_light }highlighted_less{% else %}highlighted{% endif %}">Highlighted row</div>
    + <div class="row{% if needs_more_light }highlighted_more{% else %}highlighted{% endif %}">Highlighted row</div>


#### Yammy template diff

    -            highlighted_less
    +            highlighted_more

### Compact resulting web pages

The Yammy translator produces compact HTML code without extra space characters.


Syntax Highlighting
===================

At this moment there are Yammy syntax highlighting files for the Sublime Text 2
editor and Colorer Eclipse plugin. You may find the required files and
installation instructions for each eaditor in in **editors** folder. 
