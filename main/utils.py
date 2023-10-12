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

