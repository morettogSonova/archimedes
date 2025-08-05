import country_converter as coco

def tolerant_country_code_conversion(country_code: str) -> str:
    """
    Converts a country code to its ISO3 equivalent, returning None if not found.
    """
    if country_code == 'SU':
        return 'RUS'
    elif country_code == 'CS':
        return 'CZE'
    elif country_code == 'YU':
        return 'SRB'
    elif country_code == 'DD':
        return 'DEU'
    elif country_code == 'ZR':
        return 'COD'
    elif country_code == 'EU' or country_code == 'EP':
        return 'EUR'
    elif country_code == 'OA':
        return 'AFR'
    return coco.convert(country_code, to='ISO3', not_found=None)
