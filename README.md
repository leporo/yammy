Yammy: A better way to create a Django/Jinja2 template
=====================================================

Yammy is an indent-based syntax for nice and clean templates of HTML pages.
It also uses CSS-like selectors to define HTML tags.

Yammy translator is not a template engine. It does not handle expressions or condition blocks.
It runs as a preprocessor for actual template engine like Jinja2, Twig or Django template engine.

Yammy comes with integration modules for Jinja2 and Django template engines.

There also is a command-line utility which can be used to convert Yammy template to HTML template.

Why Did We Started It
=====================

Yammy was started as an experiment aimed to solve template merge troubles.

We often had a situations like this:

* some guy adds some classes or markups used by Javascript he develops,
* other guy fixes a browser-related issue by changing the same template lines,
* and their work gets totally ruined when it comes to merge and resolving of merge conflicts.

There were far too many merge conflicts because of all those really long lines with tons of {% if's %} in HTML tag attributes.

There were far too many characters on changed lines to understand what other developer did and how the merged code should look like.

We started with the following thoughts:

* It's much easier to solve conflicts in source files then in HTML templates simply because lines in source files are much shorter;
* It would be better to use indentation for nested tags just to stop loosing and misplacing closing tags,
* It would be better to use indentation just to make templates look great,
* We don't need all those <>'s and ""'s - keep them for browsers;
* Browsers don't need all those spaces and line breaks - keep them for developers;
* It would be great to use the CSS selectors to define HTML tags and attributes,
* There is no need for full HTML syntax support, one should be able to use HTML code in Yammy template if needs to.

Then we used YAML syntax as a base and got the name for the project: Yammy.

After a brief discussion we had an idea on template syntax, then we got an implementation and it worked for us surprisingly well.

Syntax
======

The Yammy template syntax has much in common with the HAML, Slim and some other indent-based template engine languages.

Line meaning is being recognized by the first line's character:

 * Lines starting with lowercase Latin letters are HTML tags.
 * Lines starting with the '-' character are HTML tag attributes.
 * Lines starting with the '|' (pipe character) define the HTML code and the text that occurs between that element's opening and closing tag.
 * Lines starting with the '#' character are comments.
 * Lines starting with the '!' character are multi-line escaping switchers.

Empty lines and trailing spaces are ignored.

You may use CSS-like selectors to define tag's attributes.

You may also use HTML code in Yammy templates so you can easily paste some generated HTML lines into Yammy template never caring of translating it into Yammy syntax.

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
            Some text

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
    html                      <html><body><div>            <p>Hello!</p>
        body                  <p>World!</p></div></body></html>
            div
                !HTML
                <p>Hello</p>
                !YAMMY
                p World!

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

Yammy translator produces compact HTML code without extra space characters.

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


Command-Line Utility
--------------------

You may use the **yammy** command-line utility for the batch processing of
Yammy templates:

    yammy <source file or folder> [--dest=<destination file or folder name>]

I used it in PHP projects to convert .ymy files to Twig templates.

Integration
===========

Yammy integrates with Django, Jinja2 and Jingo (and any other thing you want).
Make sure you use .ymy or .yammy extension for your Yammy template files. 
Note you can also mix Yammy templates with HTML ones.  


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


Jingo Integration
-----------------

Jingo (http://pypi.python.org/pypi/jingo) is an adapter for using Jinja2
templates within Django.

The simpliest way to attach Yammy templates to Jingo adapter is by using the
**yammy.jingo_loaders** module.  

Change the TEMPLATE_LOADERS setting in your settings.py as follows:

    TEMPLATE_LOADERS = (
        'yammy.jingo_loaders.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

This code also integrates Jingo/Jinga2 to your Django project.

Syntax Highlighting
===================

At this moment there are Yammy syntax highlighting files for the Sublime Text 2
editor and Colorer Eclipse plugin.

Sublime Text
------------

Use [Package Control](http://wbond.net/sublime_packages/package_control) to install the [Yammy Syntax Highlighting](https://github.com/leporo/SublimeYammy) package.

PyCharm
-------

Clone the Sublime Text [Yammy Syntax Highlighting](https://github.com/leporo/SublimeYammy) package from GitHub repository and register this folder to the list of TextMate packages in PyCharm settings.

Make sure to define the IDE to TextMate color scheme map for Default scheme or you may get a package loading error.

Eclipse
-------

You may find the Colorer Eclipse plugin files and installation instructions in **editors/eclipse-colorer** folder. 
