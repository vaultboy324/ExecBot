import json


class ErrorParser:
    @staticmethod
    def args_parse(args: list):
        return json.loads(args[0])['Error']

    @staticmethod
    def from_list_to_string(err_messages: list):
        err_string = ''

        for err_message in err_messages:
            err_string += f'{err_message}\n'
        return err_string

    pass
