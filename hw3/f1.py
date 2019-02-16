class RegParser:
    ADDRESS_REGEX = r'^(?:[A-Z][a-z]+, )?[A-Z][a-z]+(?: [Cc]ity)?, [-A-Za-z _\d]+(?: str\.)?, \d+ *[-\/\\,|] *\d+$'
    CONTACT_REGEX = r'^(?:(?:name=(?P<name>[-\w ]*)|surname=(?P<surname>[-\w ]*)|age=(?P<age>[-\w ]*)|city=(?P<city>[-\w ]*))(?:;|$)){1,4}(?<!;)$'
    PRICE_REGEX = r'(?:(?<=[$€] )\d+(?:[,\.]\d+)?)|(?:\d+(?:[,\.]\d+)?(?= *BYN))'

    @classmethod
    def find(cls, s, n):
        if n == 1:
            return re.findall(cls.ADDRESS_REGEX, s, flags=re.MULTILINE)
        if n == 2:
            return [
                {k: v for k, v in item.groupdict().items() if v}
                for item in re.finditer(
                    cls.CONTACT_REGEX,
                    s,
                    flags=re.MULTILINE
                )
            ]
        if n == 3:
            return [
                float(item.replace(',', '.')) if any(
                    s in item for s in '.,'
                ) else int(item)
                for item in re.findall(
                    cls.PRICE_REGEX,
                    s,
                    flags=re.MULTILINE
                )
            ]
