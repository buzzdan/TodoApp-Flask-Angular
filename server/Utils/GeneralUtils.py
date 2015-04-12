from server.Utils.Exceptions import InvalidInstantiationError


def member_exists(obj, member, of_type):
    member_value = getattr(obj, member, None)

    if member_value is None:
        return False

    if not isinstance(member_value, of_type):
        return False

    return True


def must_have(obj, member, of_type, use_method):
        if not member_exists(obj, member, of_type=of_type):
            raise InvalidInstantiationError(obj.__class__.__name__,
                                            member,
                                            of_type.__name__,
                                            use_method)