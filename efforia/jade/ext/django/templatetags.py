"""
A smarter {% if %} tag for django templates.

While retaining current Django functionality, it also handles equality,
greater than and less than operators. Some common case examples::

    {% if articles|length >= 5 %}...{% endif %}
    {% if "ifnotequal tag" != "beautiful" %}...{% endif %}
"""
import unittest
#import efforia.jade as jade
from django import template

register = template.Library()

@register.tag(name="__jade_attrs")
def do_evaluate(parser, token):
  '''Calls an arbitrary method on an object.'''
  code = token.contents
  firstspace = code.find(' ')
  if firstspace >= 0:
    code = code[firstspace+1:]
  return Evaluator(code)

class Evaluator(template.Node):
  '''Calls an arbitrary method of an object'''
  def __init__(self, code):
    self.code = code
    
  def render(self, context):
    '''Evaluates the code in the page and returns the result'''
    modules = {
      'jade': __import__('efforia.jade.runtime',globals(),locals(),['attrs'])
    }
    context['false'] = False
    context['true'] = True
    return str(eval('jade.attrs(%s)'%self.code,modules,context))

@register.tag(name="__jade_set")
def do_set(parser, token):
  '''Calls an arbitrary method on an object.'''
  code = token.contents
  firstspace = code.find(' ')
  if firstspace >= 0:
    code = code[firstspace+1:]
  return Setter(code)

class Setter(template.Node):
  '''Calls an arbitrary method of an object'''
  def __init__(self, code):
    self.code = code
    
  def render(self, context):
    '''Evaluates the code in the page and returns the result'''
    modules = {
    }
    context['false'] = False
    context['true'] = True
    new_ctx = eval('dict(%s)'%self.code,modules,context)
    context.update(new_ctx)
    return ''

if __name__ == '__main__':
    unittest.main()
