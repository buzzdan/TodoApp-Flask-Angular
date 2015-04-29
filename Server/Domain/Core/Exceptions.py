class InvalidInstantiationError(Exception):
    def __init__(self, origin_class_name, missing_argument_name, missing_argument_type, instantiation_method_to_use=None):

        message = """Invalid object instantiation - missing instantiation argument:
         class name: '{class_name}'
         argument name: '{arg}'
         argument type: '{arg_type}"""\
            .format(class_name=origin_class_name,
                    arg=missing_argument_name,
                    arg_type=missing_argument_type)

        if instantiation_method_to_use:
            message += """
            Please use the '{method_name}' factory class method"""\
                .format(method_name=instantiation_method_to_use)

        # Call the base class constructor with the parameters it needs
        super(InvalidInstantiationError, self).__init__(message)


class PreConditionError(Exception):
    def __init__(self, origin_method_name, missing_argument_name, missing_argument_type):

        message = """Invalid precondition argument:
         method: '{method_name}'
         argument name: '{arg}'
         argument type: '{arg_type}'"""\
            .format(class_name=origin_method_name,
                    arg=missing_argument_name,
                    arg_type=missing_argument_type)

        # Call the base class constructor with the parameters it needs
        super(InvalidInstantiationError, self).__init__(message)