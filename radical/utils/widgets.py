# coding=utf-8
from django import forms
from django.forms.utils import flatatt
from htmlmin.util import force_text


class MediaMixin(object):
    class Media:
        css = {'screen': ('/static/admin/css/charsleft.css',), }
        js = ('/static/admin/js/charsleft.js',)


class CharsLeftInput(forms.TextInput, MediaMixin):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(self.attrs, {'type': self.input_type,
                                                    'name': name})
        if value != '':
            final_attrs['value'] = force_text(value)
        maxlength = final_attrs.get('maxlength', False)
        current = force_text(len(value))

        html = '<div class="charsleft charsleft-input">' \
               '   <input {}/>' \
               '   <div class="counter"><small class="count">{}</small> <small>de {}</small></div>' \
               '</div>'.format(
            flatatt(final_attrs),
            current,
            int(maxlength)
        )

        return html
