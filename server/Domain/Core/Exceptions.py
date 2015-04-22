class InvalidInstantiationError(Exception):
    def __init__(self, origin_class_name, missing_argument_name, missing_argument_type, instantiation_method_to_use=None):

        message = """Invalid instantiation for class '{class_name}':
                  missing instantiation argument '{arg}' of type '{arg_type}'."""\
            .format(class_name=origin_class_name,
                    arg=missing_argument_name,
                    arg_type=missing_argument_type)

        if instantiation_method_to_use:
            message += """
            Please use the '{method_name}' factory class method"""\
                .format(method_name=instantiation_method_to_use)

        # Call the base class constructor with the parameters it needs
        super(InvalidInstantiationError, self).__init__(message)