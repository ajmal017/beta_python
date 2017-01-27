
from datetime import date

def Serialize(object, inline = False, field_list = None, serialize_underlying = True):
    xmldoc = ""
    if field_list is None:
        field_list = object.__dict__
    for field in field_list:
        if not field.startswith("_") and not object.__dict__[field] is None and field not in ["id","idx"] and not field.endswith("_ptr_id"):
            if field.endswith("_id") and not object.__dict__[field] is None and "_"+field[:-3]+"_cache" in object.__dict__:
                if serialize_underlying:
                    related_object = object.__dict__["_"+field[:-3]+"_cache"]
                    if type(related_object) is list:
                        for related_object_item in related_object:
                            xmldoc +='\n\r'+related_object_item.__str__(field[:-3])
                    else:
                        xmldoc+='\n\r'+related_object.__str__(field[:-3])
            elif inline:
                xmldoc += ' '+field + '=' + ToStr(object.__dict__[field], True)
            else:
                xmldoc += '\n\r<' + field + '>' + ToStr(object.__dict__[field], False) + '</' + field + '>'
    return xmldoc

def ToStr(object, use_quotes):
    q =''
    if use_quotes:
        q = '"'
    if type(object) is str:
        return q+object+q
    elif type(object) is date:
        return q + str(object) + q
    elif type(object) is bool:
        return q + str(object) + q
    else:
        return str(object)