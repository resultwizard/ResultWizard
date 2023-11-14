def snake_case_to_camel_case(snake_case_name: str):
    name_parts = snake_case_name.split("_")
    camel_case_name = name_parts[0]
    for name_part in name_parts[1:]:
        camel_case_name += name_part[0].upper() + name_part[1:]
    return camel_case_name


def round_to_n_decimal_places(v: float, n: int):
    return "{:.{}f}".format(v, int(n))
