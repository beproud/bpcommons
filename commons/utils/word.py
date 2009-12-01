# vim:fileencoding=utf8
from datetime import date,datetime,timedelta
import MeCab
import re
import zenhan

ignore_re = re.compile(ur'^[－ ゜゜゜...,あ-ん０１２３４５６７８９、。、・・￥？ ﾟ]{1,2}$')
ignore_re2 = re.compile(ur'^[a-z0-9()\-!"#$%&\'\"()^^)]{1,2}$')
def extract_word(content):
    m = MeCab.Tagger ("-Owakati")
    n = m.parseToNode(content)
    n = n.next
    l = []
    while n:
        cs = n.feature.split(",")[0]
        #print cs,n.surface
        if cs in ('名詞','形容詞','動詞'):
            s = unicode(n.surface.lower() ,'utf8')
            s = optimize_word(s)
            if (cs in ('動詞') and len(s) < 2) or ignore_re.match(s) or ignore_re2.match(s):
                n = n.next
                continue
            l.append(s)
        n = n.next
    return l

RE_EXTRACT = re.compile(u'名詞')
RE_URL = re.compile(r'(http(s)?:\/\/[A-Za-z0-9%&=~?+-_/.#]+)')
RE_EXTRACT_IGNORE = re.compile(ur'^[()\-!?"#$%&\'\",.;ー]')
RE_EXTRACT_IGNORE_KANA = re.compile(ur'^[あ-ん０１２３４５６７８９]+$')
def extract_keywords(content):
    """
    キーワード抽出
    """
    m = MeCab.Tagger("-Ochasen")
    n = m.parseToNode(RE_URL.sub(',', optimize_word(content)).encode('utf8'))
    d = {}
    w = u''
    score = 0
    while n:
        features = unicode(n.feature, 'utf8').split(',')
        # 名詞を抽出
        surface = unicode(n.surface, 'utf8')
        if RE_EXTRACT.match(features[0]) and not RE_EXTRACT_IGNORE.match(surface):
            w += surface
            score += 1
        else:
            if w:
                if len(w) >= 2 and not RE_EXTRACT_IGNORE_KANA.match(w):
                    if not w in d:
                        d[w] = 0
                    d[w] += 1 #score
                w = u''
                score = 0
        n = n.next
    # ソート
    def cmp_keywords(i1, i2):
        if i1[1] == i2[1]:
            # 長さが同じ場合
            try:
                if content.index(i1[0]) < content.index(i2[0]):
                    return 1
            except:
                return -1
            return -1
        return cmp(i1[1], i2[1])

    return sorted(d.items(), cmp=cmp_keywords, reverse=True)

def optimize_word(w):
    """
    全角記号英数字を半角に、半角かなを全角に
    """
    w = zenhan.z2h(w, zenhan.ASCII)
    return zenhan.h2z(w, zenhan.KANA)

def optimize_content(s):
    """
    コンテンツの半角カナを全角に
    """
    return zenhan.h2z(s, zenhan.KANA)

trim_re = re.compile(u'^[\s\u3000]+|[\s\u3000]+$')
def trim_content(s):
    """
    コンテンツのtrim
    """
    return trim_re.sub(u'', s)

def hankaku(s):
    s = zenhan.z2h(s, zenhan.ASCII)
    return zenhan.z2h(s, zenhan.KANA)

def normalize_content(w):
    """
    全角記号英数字を半角に、半角かなを全角に
    全角数字を半角数字に
    全角の[ー－―‐]を - に
    """
    w = re.sub(u'[\u30FC\uFF0D\u2015\u2010]', '-', w)
    w = zenhan.z2h(w, zenhan.ASCII | zenhan.DIGIT)
    return zenhan.h2z(w, zenhan.KANA)
