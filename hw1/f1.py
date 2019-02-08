MaxMin = collections.namedtuple('MaxMin', 'max_value min_value')

def get_max_and_min(
    data: typing.Set[typing.Union[decimal.Decimal, fractions.Fraction, str]]
) -> typing.NamedTuple:
    d = []
    for item in data:
        if isinstance(item, str):
            if ' \\ ' in item:
                d.append(fractions.Fraction(item.replace(' \\ ', '/')))
            else:
                d.append(decimal.Decimal(item))
        else:
            d.append(item)
    return MaxMin(max(d), min(d))
