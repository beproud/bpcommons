# vim:fileencoding=utf-8
import re

RE_KEYWORD_EXTRACT = re.compile(u'名詞')
RE_KEYWORD_URL = re.compile(r'(http(s)?:\/\/[A-Za-z0-9%&=~?+-_/.#]+)')
RE_KEYWORD_EXTRACT_IGNORE = re.compile(ur'^[()\-!?"#$%&\'\",.;ー]')
RE_KEYWORD_EXTRACT_IGNORE_KANA = re.compile(ur'^[あ-ん０１２３４５６７８９]+$')
RE_NORMALIZE = re.compile(u'[\u30FC\uFF0D\u2015\u2010]')

__all__ = (
    'extract_keywords',
    'optimize',
    'hankaku',
    'normalize',
)

def extract_keywords(s, cmpfunc=None, dic_encoding='utf-8'):
    """
    キーワード抽出
    """
    import MeCab
    m = MeCab.Tagger("-Ochasen")
    n = m.parseToNode(RE_KEYWORD_URL.sub(',', optimize(s)).encode(dic_encoding))
    d = {}
    w = u''
    score = 0
    while n:
        features = unicode(n.feature, dic_encoding).split(',')
        # 名詞を抽出
        surface = unicode(n.surface, dic_encoding)
        if RE_KEYWORD_EXTRACT.match(features[0]) and not RE_KEYWORD_EXTRACT_IGNORE.match(surface):
            w += surface
            score += 1
        else:
            if w:
                if len(w) >= 2 and not RE_KEYWORD_EXTRACT_IGNORE_KANA.match(w):
                    if not w in d:
                        d[w] = 0
                    d[w] += 1 #score
                w = u''
                score = 0
        n = n.next
    # ソート
    if cmpfunc:
        cmp_keywords = cmpfunc
    else:
        def cmp_keywords(i1, i2):
            if i1[1] == i2[1]:
                # 長さが同じ場合
                try:
                    if s.index(i1[0]) < s.index(i2[0]):
                        return 1
                except:
                    return -1
                return -1
            return cmp(i1[1], i2[1])

    return sorted(d.items(), cmp=cmp_keywords, reverse=True)

def optimize(s):
    """
    全角記号英数字を半角に、半角かなを全角に
    """
    import zenhan
    s = zenhan.z2h(s, zenhan.ASCII)
    return zenhan.h2z(s, zenhan.KANA)

def hankaku(s):
    import zenhan
    s = zenhan.z2h(s, zenhan.ASCII)
    return zenhan.z2h(s, zenhan.KANA)

def normalize(s):
    """
    全角記号英数字を半角に、半角かなを全角に
    全角数字を半角数字に
    全角の[ー－―‐]を - に
    """
    import zenhan
    s = RE_NORMALIZE.sub('-', s)
    s = zenhan.z2h(s, zenhan.ASCII | zenhan.DIGIT)
    return zenhan.h2z(s, zenhan.KANA)
