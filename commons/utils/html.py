# vim:fileencoding=utf-8
import re

from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.conf import settings

__all__ = (
    'sanitize_html',
    'urlize',
)

VALID_TAGS = getattr(settings, "STRIPPER_VALID_TAGS",
    {
        'b': (),
        'blockquote': ('style',),
        'em': (),
        'strong': (),
        'strike': (),
        'a': ('href', 'title'),
        'i': (),
        'br': (),
        'ul': (),
        'ol': (),
        'li': (),
        'u': (),
        'p': (),
        'h1': (),
        'h2': (),
        'h3': (),
        'h4': (),
        'table': (),
        'thead': (),
        'tbody': (),
        'tfoot': (),
        'th': (),
        'td': ('colspan',),
        'tr': ('rowspan',),
        'hr': (),
        'img': ('src', 'alt', 'title', 'width', 'height', 'align'),
        'span': ('style',),
        'div': ('style',),
        'font': ('size', 'style', 'color'),
    }
)

VALID_STYLES = getattr(settings, "STRIPPER_VALID_STYLES", (
        "background-color",
        "color",
        "margin",
        "margin-left",
        "margin-right",
        "border",
        "padding",
        "font-weight",
        "font-style",
        "font-size",
        "text-align",
        "text-decoration",
    )
)

RE_ANCHOR_STR = ur'(http[s]*\:\/\/.%s)(,|&gt;|&lt;|<|>|\s| |　|\xe3\x80\x80|$)'
RE_ANCHOR_NOLIMIT = re.compile(anchor_re_str % "+?")
RE_ANCHOHR_RES_STR = ur'<a href="\1"%s>\1</a>\2'

def sanitize_html(htmlSource, encoding=None):
    """
    Clean bad html content. Currently this simply strips tags that
    are not in the VALID_TAGS setting.
    
    This function is used as a replacement for feedparser's _sanitizeHTML
    and fixes problems like unclosed tags and gives finer grained control
    over what attributes can appear in what tags.

    Returns the sanitized html content.
    """
    from BeautifulSoup import BeautifulSoup, Comment

    js_regex = re.compile(r'[\s]*(&#x.{1,7})?'.join(list('javascript')))
    css_regex = re.compile(r' *(%s): *([^;]*);?' % '|'.join(VALID_STYLES), re.IGNORECASE)
    domain_regex = re.compile(r"^ *http\://(?!%s)" % re.escape(settings.DOMAIN)) 
    # Sanitize html with BeautifulSoup
    if encoding:
        soup = BeautifulSoup(htmlSource, fromEncoding=encoding)
    else:
        soup = BeautifulSoup(htmlSource)

    def entities(text):
        return text.replace('<','&lt;')\
                   .replace('>', '&gt;')\
                   .replace('"', '&quot;')\
                   .replace("'", '&apos;')
    
    # Sanitize html text by changing bad text to entities.
    # BeautifulSoup will do this for href and src attributes
    # on anchors and image tags but not for text.
    for text in soup.findAll(text=True):
        text.replaceWith(entities(text))

    # コメントを削る
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.hidden = True
        else:
            tag.attrs = [(attr, js_regex.sub('', val))
                            for attr, val in tag.attrs 
                            if attr in VALID_TAGS[tag.name]]

    # リンクに rel="nofollow"を追加
    for tag in soup.findAll("a", attrs={"href":domain_regex}):
        tag["rel"] = "nofollow" 

    # CSSを整理
    for tag in soup.findAll(attrs={"style":re.compile(".*")}):
        style = ""
        for key,val in css_regex.findall(tag["style"]):
            style += "%s:%s;" % (key,val.strip())
        tag["style"] = style

    return soup.renderContents().decode('utf8') 

def urlize(text, trim_url_limit=None, nofollow=False, autoescape=False):
    """text内URLを抽出してアンカータグで囲む
    
    URLのデリミタは半角カンマ、<>(エスケープ済み含む)、\s、全角スペース、行末で、これらが末尾にマッチしない場合はURLとして認識しません。
    URL部分は.+の最小マッチ、もしくはtrim_url_limitが指定された場合は{,trim_url_limit}の最小マッチとなります。

    -args

        text:           urlize対象文字列
        trim_url_limit: urlとして認識する文字数に上限を設ける場合は数値をセット
        nofollow:       Trueを与えるとタグにrel="nofollow"を付加
        autoescape:     Trueを与えるとタグエスケープを行います。
    
    """
    if autoescape:
        text = escape(text)

    if trim_url_limit:
        anchor_re = re.compile(RE_ANCHOR_STR % "{,%s}?" % trim_url_limit)
    else:
        anchor_re = RE_ANCHOR_NOLIMIT

    if nofollow:
        anchor_re_result = RE_ANCHOHR_RES_STR % ' rel="nofollow"'
    else:
        anchor_re_result = RE_ANCHOHR_RES_STR % ""

    return anchor_re.sub(anchor_re_result, text)
