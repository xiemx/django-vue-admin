from audit.models import UserOperationLog


def record_operation_log(func):

    def wrapper(*args, **kwargs):

        try:

            __viewset = args[0]
            __request = args[1]
            __kw = {}

            if __viewset.action == "partial_update":
                instance = __viewset.get_object()
                __kw['before'] = __viewset.get_serializer(instance).data

            if __viewset.request.user:
                __kw['user'] = __viewset.request.user

            if __viewset.action:
                __kw['operation'] = __viewset.action

            if __viewset.serializer_class.Meta.model.__name__:
                __kw['resource'] = __viewset.serializer_class.Meta.model.__name__

            if __request.data:
                __kw['content'] = __request.data

            log = UserOperationLog(**__kw)

            log.save()
        except Exception as err:
            print(err)

        return func(*args, **kwargs)

    return wrapper
