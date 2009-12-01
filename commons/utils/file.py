# vim:fileencoding=utf8

def file_extension(file_name):
    index = file_name.rfind(".")
    if index == -1:
        return ""
    else:
        return file_name[index+1:]
