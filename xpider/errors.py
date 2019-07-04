# coding=utf-8


class UsageError(Exception):
    """
    Command usage error.
    """

    def __init__(self, *args, print_help=False, **kwargs):
        self.print_help = print_help
        super().__init__(*args, **kwargs)
