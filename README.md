Yammy: A better way to create a Django/Jinja template
=====================================================

Yammy is not a template engine. The Yammy's translator does not handle expressions or condition blocks.
Yammy strips unnecessary parts from HTML template and makes the template collaboration-friendly.  

Basic Usage
-----------

Yammy Template → Django/Jinja HTML Template → Web Page

    >>> from yammy import yammy_to_html
    >>> yammy_to_html('template.yammy', 'template.html')
    
    >>> from yammy import yammy_to_html_string
    >>> yammy_to_html_string('div\n    | Inner text')

Jinja2 Integration
------------------

Yammy comes with the Jinja2 integration module.
The simplest way to enable a Yammy template processing in your application looks roughly like this:

    from jinja2 import Environment
    from yammy import YammyPackageLoader
    env = Environment(loader=YammyPackageLoader('yourapplication', 'templates'))

Make sure you use .ymy or .yammy extension for your Yammy template files. 
Note you can also mix Yammy templates with HTML ones.  

Syntax
------

The Yammy template syntax has much in common with the HAML, Slim and many other similar template engine languages.

Line meaning is being recognized by the first line's character:

 * Lines starting with Latin letters are HTML tags.
 * Lines starting with the '-' character are HTML tag attributes.
 * Lines starting with the '|' (pipe character) define the HTML code and the text that occurs between that element's opening and closing tag.
 * Lines starting with the '#' character are comments.

Empty lines and trailing spaces are ignored.


### HTML Tags

    Yammy                     HTML
    ------------------------- -----------------------------------------------------------
    div Some Text             <div>Some text</div>
    
    div                       <div>Some text</div>
        | Some text


### HTML Attributes

    Yammy                     HTML
    ------------------------- -----------------------------------------------------------
    
    div.class#id Inner Text   <div class="class" id="id">Inner Text</div>

    div                       <div class="class" id="id">Inner Text</div>
        - class class
        - id id
        | Inner Text
    
    div."class1 class2"#id    <div class="class1 class2" id="id">Inner Text</div>
    
    input[type="submit"]      <input type="submit"/>


### Nesting

Tag nesting is being declared using indentation:

    Yammy                     HTML
    ------------------------- -----------------------------------------------------------
    div.outer                 <div class="outer"><div class="inner">Some text</div></div>
        div.inner
            | Some text

### Template engine statements and plain HTML

    Yammy                     HTML
    ------------------------- -----------------------------------------------------------
    <!doctype html>           <!doctype html><html><body></body></html>
    html
        body
    
    {% if target.hit %}       {% if target.hit %}<div class="hit">Hit!</div>{% endif %}
        div.hit Hit!
    {% endif %}

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
----------

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