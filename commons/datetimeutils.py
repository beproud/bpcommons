# vim:fileencoding=utf8
import calendar
import time
import rfc822
from datetime import date,datetime,timedelta

def utc_to_local(utc_date_str):
    """
    rfc822 UTC date string => local datetime obj
    """
    return datetime(*time.localtime(calendar.timegm(rfc822.parsedate(utc_date_str)))[:6])

def relative_time(s, shortname=False):
    now = datetime.now()
    diff = now - s
    if now < s or (diff.days < 1 and diff.seconds < 1):
        return u"たった今" 
    if diff.days > 0:
        if shortname:
            return s.strftime("%m-%d")
        else:
            return s.strftime("%Y-%m-%d %H:%M")
    elif diff.seconds > 60*60:
        hours = diff.seconds >= 60*30 and (diff.seconds / 3600) + 1 or (diff.seconds / 3600) 
        str = u"%s時間前" % (hours)
    elif diff.seconds > 60:
        minutes = diff.seconds >= 30 and (diff.seconds / 60)+1  or (diff.seconds / 60)
        str = u"%s分前" % (minutes)
    else :
        str = u"%s秒前" % (diff.seconds)
    return str

def repr_time_status(diff):
    """
    回答受付期間を文字列で返す
    """
    
    if diff < timedelta(0):
        str = u'終了'
    elif diff.days > 0:
        days = diff.seconds >= 60*60*12 and diff.days+1 or diff.days
        str = u"あと%s日" % (days)
    elif diff.seconds > 60*60:
        hours = diff.seconds >= 60*30 and (diff.seconds / 3600) + 1 or (diff.seconds / 3600) 
        str = u"あと%s時間" % (hours)
    else :
        minutes = diff.seconds >= 30 and (diff.seconds / 60)+1  or (diff.seconds / 60)
        str = u"あと%s分" % (minutes)
    return str

