Yammy: A better way to create a Django/Jinja template
=====================================================

Yammy is not a template engine. It does not handle expressions or condition blocks.
It just provides another way to create and maintain an HTML template.

    Yammy Template → Django/Jinja HTML Template → Web Page

Advantages
----------

### Readability

There are no extra brackets and quotes. Block nesting is defined by their indentation.

### Better collaboration

It's hard to work on the same HTML template with someone else.
Changes made to long lines with many attribute definitions are difficult to merge.
Nested single row condition statements are difficult to understand and maintain.

With Yammy you may split your template to as many lines as you wish and indent nested blocks.

It's easier to figure out what has been changed:

#### HTML template diff

    - <div class="row{% if needs_more_light }highlighted_less{% else %}highlighted{% endif %}">Highlighted row</div>
    + <div class="row{% if needs_more_light }highlighted_more{% else %}highlighted{% endif %}">Highlighted row</div>


#### Yammy template diff

    -            highlighted_less
    +            highlighted_more

### Compact resulting web pages

The Yammy translator produces a compact HTML code without extra space characters.
With Yammy you'll never have a HTML code like this on your site:

    <div>
    
    
    
        <div>
    The first line.
      <br/>

            The second line.
        
        </div>
    
    
    
    
    </div>

Usage
-----

    >>> from yammy import yammy_to_html
    >>> yammy_to_html('template.yammy', 'template.html')
    
    >>> from yammy import yammy_to_html_string
    >>> yammy_to_html_string('div\n    | Inner text')

Syntax
------

The Yammy syntax has much in common with the HAML, Slim and many other similar template engine languages.

Lines are recognized by the first character:

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

### Nesting

Tags are nested with indentation.

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

Yammy does not support multiline comments. Lines starting with the '#' (hash character) will be ignored.

    Yammy                     HTML
    ------------------------- -----------------------------------------------------------
    div                       <div class="class" id="id">Inner Text</div>
        # define class
        - class class
        # specify id
        - id id
        # write inner text
        | Inner Text

Sample
------

    ol.someclass#some_id
      li.item
        - style
            color:black;
            background:
            {% if error %}
              red;
            {% else %}
              {% if warning %}
                yellow;
              {% else %}
                transparent;
              {% endif %}
            {% endif %}
        - title 
          some extra information

        | First item text
        | Next Line text

      li.item Second item text

      li
        - class
            item
          {% if last_item %}
            last_item_class
          {% endif %}
        |Not yet

      li."item last_item_class"
        |Third item text
