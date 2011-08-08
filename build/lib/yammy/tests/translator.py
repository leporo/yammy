from yammy.translator import yammy_to_html_string


def test_translate_string(input):
	""" A Simple proxy for the yammy_to_html_string function
	
	>>> test_translate_string('div.class#id some text')
	'<div id="id" class="class">some text</div>'
	>>> test_translate_string('\\n'.join(['div', '    - class class', '    - id id', '    | some text\\n    | and next text line']))
	'<div class="class" id="id">some text and next text line</div>'
	
	"""
	return yammy_to_html_string(input)

"""
ol.someclass#some_id											<ol class="someclass" id="some_id">  
	li.item														<li class="item" style="color:black;background:{% if error %}red;{% else %}{% if warning %}yellow;{% else %}transparent;{% endif %}{% endif %}" title="some extra information">First item text</li>
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

	li.item Second item text									<li class="item">Secon item text</li>

	li															<li class="item{% if last_item %} last_item_class{% endif %}">Not yet</li>
		- class
			item
			{% if last_item %}
				last_item_class
			{% endif %}
		|Not yet


	li."item last_item_class"									<li class="item last_item_class">Third item text</li>
		|Third item text
																</ol>
"""

if __name__ == "__main__":
	import doctest
	doctest.testmod()