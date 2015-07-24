import re
from django import forms
from django.template.loader import render_to_string


class PointWidget(forms.HiddenInput):
    def render(self, name, value, attrs):
        rendered = super(PointWidget, self).render(name, value, attrs)

        self.attrs['id'] = attrs['id']
        self.attrs.setdefault('google_map_version', '3.exp')
        self.attrs.setdefault('base_lat', '37.497921')  # Gangnam Station
        self.attrs.setdefault('base_lng', '127.027636')
        self.attrs.setdefault('width', '100%')
        self.attrs.setdefault('height', 300)

        self.attrs['width'] = str(self.attrs['width'])
        if self.attrs['width'].isdigit():
            self.attrs['width'] += 'px'

        self.attrs['height'] = str(self.attrs['height'])
        if self.attrs['height'].isdigit():
            self.attrs['height'] += 'px'

        if value:
            try:
                lng, lat = re.findall(r'[-\d\.]+', value)
                self.attrs['base_lat'] = lat
                self.attrs['base_lng'] = lng
            except (IndexError, ValueError):
                pass

        html = render_to_string('blog/point_widget.html', self.attrs)
        return rendered + html
