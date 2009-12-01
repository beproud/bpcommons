#coding=utf8
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from django.core.files.base import ContentFile
from PIL import Image
import re
import os

def valid_image(image):
    try:
        Image.open(image)
    except IOError:
        return False
    image.seek(0)
    return True

def make_content_image_file(image, size=None):
    """ """
    format = image.format
    if size:
        image = image.resize(size,Image.ANTIALIAS);
    sio = StringIO()
    image.save(sio, format)
    return ContentFile(sio.getvalue());


def optimize_resize(image,size):
    frm = image.format
    w,h = image.size
    box = () 
    if w < h :
        s = (h-w) / 2
        box = (0,s,w,s+w)
    else :
        s = (w-h) / 2
        box = (s,0,s+h,h)
    image = image.crop(box)
    image = image.resize(size,Image.ANTIALIAS)
    return image

def get_image_size(fileobj, limit=None):
    image = Image.open(fileobj)
    w, h = image.size
    if limit:
        if max(w, h) > limit:
            if w > h:
                h = h * limit / w
                w = limit
            else:
                w = w * limit / h
                h = limit
    return w, h

class ImageSizeNameConverter(object):
    @classmethod
    def add_upload_to(cls,path,upload_to):
        paths = path.split(os.sep)
        paths.insert(-1,upload_to)
        return os.sep.join(paths)

    @classmethod
    def convert(cls,prefix,path,upload_to=None):
        if upload_to:
            path = cls.add_upload_to(path,upload_to)
        paths = path.split(os.sep)
        paths[-1] = "%s__%s" % (prefix,paths[-1])
        return os.sep.join(paths)
        
    @classmethod
    def revert(cls,prefix,path):
        import string
        paths = path.split(os.sep)
        r = re.compile("^"+prefix+"__")
        paths[-1] = r.sub("",paths[-1])
        return os.sep.join(paths)

multiple_sizename_converter = ImageSizeNameConverter


