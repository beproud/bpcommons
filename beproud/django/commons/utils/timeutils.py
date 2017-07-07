# vim:fileencoding=utf-8
from __future__ import division
import time
import calendar
from datetime import datetime, timedelta

SEC_1_MINUTES = 60
SEC_1_HOURS = SEC_1_MINUTES * 60

__all__ = (
    'utc_to_local',
    'relative_time',
    'times_left',
)

def utc_to_local(utc_datetime):
    """
    UTC datetime obj => local datetime obj
    """
    return datetime(*time.localtime(calendar.timegm(utc_datetime.timetuple()))[:6])

def relative_time(d, basetime=None, shortname=False, delta=None):
    """
    経過時間を表す文字列
    """
    if not delta:
        basetime = basetime or datetime.now()
        delta = basetime - d
    if basetime < d or (delta.days < 1 and delta.seconds < 1):
        return u"たった今"
    if delta.days > 0:
        if shortname:
            return d.strftime("%m-%d")
        else:
            return d.strftime("%Y-%m-%d %H:%M")
    elif delta.seconds > SEC_1_HOURS:
        hours = delta.seconds >= SEC_1_MINUTES * 30 and (delta.seconds // SEC_1_HOURS) + 1 or (delta.seconds // SEC_1_HOURS)
        result = u"%s時間前" % (hours)
    elif delta.seconds > SEC_1_MINUTES:
        minutes = delta.seconds >= 30 and (delta.seconds // SEC_1_MINUTES) + 1  or (delta.seconds // SEC_1_MINUTES)
        result = u"%s分前" % (minutes)
    else :
        result = u"%s秒前" % (delta.seconds)
    return result

def times_left(d, basetime=None, delta=None):
    """
    残り時間を表す文字列
    """
    if not delta:
        basetime = basetime or datetime.now()
        delta = d - basetime
    if delta < timedelta(0):
        result = u'終了'
    elif delta.days > 0:
        days = delta.seconds >= SEC_1_HOURS * 12 and delta.days + 1 or delta.days
        result = u"あと%s日" % (days)
    elif delta.seconds > SEC_1_HOURS:
        hours = delta.seconds >= SEC_1_MINUTES * 30 and (delta.seconds // SEC_1_HOURS) + 1 or (delta.seconds // SEC_1_HOURS)
        result = u"あと%s時間" % (hours)
    else:
        minutes = delta.seconds >= 30 and (delta.seconds // SEC_1_MINUTES) + 1  or (delta.seconds // SEC_1_MINUTES)
        result = u"あと%s分" % (minutes)
    return result
