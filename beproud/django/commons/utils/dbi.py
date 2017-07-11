# vim:fileencoding=utf-8

from six import iteritems


def select(connection, sql, params=None, model=None):
    """
    SQLを実行してmodelに値を入れる
    connectionがPythonDBIに対応していれば利用可能
    """
    cur = connection.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    columns = [column_info[0] for column_info in cur.description]
    raw_results = cur.fetchall()

    dict_results = []
    if not raw_results:
        return []
    for row in raw_results:
        dict_results.append(dict(zip(columns, row)))
    if model is None:
        return dict_results

    obj_results = []
    for item in dict_results:
        instance = model()
        for key, value in iteritems(item):
            setattr(instance, key, value)
        obj_results.append(instance)
    return obj_results
