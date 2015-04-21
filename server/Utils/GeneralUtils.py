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


def pre_condition_arg(obj, arg, of_type):
    """Making sure an argument is of a certain type.
    if not - throws InvalidInstantiationError
    :param obj: current calling object (it's name will appear in the exception if thrown)
    :param arg: argument that is passed in (to validate)
    :param of_type: of which type the argument is supposed to be
    """
    if not isinstance(arg, of_type):
            raise InvalidInstantiationError(obj.__class__.__name__,
                                            arg,
                                            of_type.__name__)