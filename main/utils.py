from loguru import logger


def show_queryset(queryset):
    """ show all fields inside a queryset object """
    if queryset:
        model = queryset.model
        fields = model._meta.fields
        for field in fields:
            logger.debug(field.name)
    else:
        logger.debug("The queryset is empty.")


def show_object(obj):
    """ show fields inside an object """
    model = obj.__class__
    fields = model._meta.fields
    for field in fields:
        field_value = getattr(obj, field.name)
        logger.debug(f"{field.name}: {field_value}")


def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output: 
           mb= 300002347.946
    """

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return("{:0.2f}".format(r))