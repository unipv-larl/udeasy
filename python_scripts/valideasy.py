import udapi


class ConlluError(Exception):
    def __init__(self, type: str, line: int, column=0):
        super().__init__()
        if type == 'integer':
            self.message = f'Error in line {line}: integer number expected in column {column}'
        elif type == 'columns':
            self.message = f'Error in line {line}: not 10 columns'
        elif type == 'missing_blank_line':
            self.message = f'Error in line {line}: missing blank line after sentence'
        elif type == 'more_blank_lines':
            self.message = f'Error in line {line}: more than one blank line after sentence'
        else:
            self.message = f'Error in line {line}: check carefully'


def validate(file_treebank: str) -> str:
    with open(file_treebank, encoding="utf8") as file:
        lines = [l.strip() for l in file.readlines()]

    blanks = 1
    meta_open = False
    passed = True
    errors = ''
    for l in lines:
        try:
            if l.startswith('#'):
                if not meta_open:
                    meta_open = True
                    if blanks > 1:
                        raise ConlluError(type='more_blank_lines', line=(lines.index(l) + 1))
                    elif blanks == 0:
                        raise ConlluError(type='missing_blank_line', line=(lines.index(l) + 1))
                    else:
                        blanks = 0
            elif not l:
                blanks += 1
            else:
                meta_open = False
                if blanks > 0:
                    raise ConlluError(type='more_blank_lines', line=(lines.index(l) + 1))
                fields = l.split('\t')
                if len(fields) != 10:
                    raise ConlluError(type='columns', line=(lines.index(l) + 1))
                else:
                        if '-' not in fields[0] and '.' not in fields[0]:
                            try:
                                int(fields[0])
                            except IndexError:
                                pass
                            except ValueError:
                                raise ConlluError(type='integer', line=(lines.index(l) + 1), column=1)
                            try:
                                int(fields[6])
                            except IndexError:
                                pass
                            except ValueError:
                                raise ConlluError(type='integer', line=(lines.index(l) + 1), column=7)
        except ConlluError as conlluerror:
            errors += conlluerror.message + '\n'
            passed = False


    if passed:
        try:
            udapi.Document(file_treebank)
        except ValueError as udapi_err:
            errors += str(udapi_err) + ' \n'

    return errors
