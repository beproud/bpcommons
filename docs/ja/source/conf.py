# -*- coding: utf-8 -*-

from datetime import date
from beproud.django.commons import VERSION


source_suffix = '.rst'
master_doc = 'index'
project = u'bpcommons'
copyright = u'{:%Y}, BeProud Inc.'.format(date.today())

version = release = VERSION

language = 'ja'

pygments_style = 'sphinx'

html_theme='classic'

