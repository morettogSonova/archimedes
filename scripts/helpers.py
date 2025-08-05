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


def tolerant_country_name_to_code_conversion(country_name: str) -> str:
    """
    Converts a country name to its ISO3 equivalent, returning None if not found.
    """
    if country_name == 'Austria-Hungary':
        return 'AUT'
    if country_name == 'West Germany':
        return 'DEU'
    if country_name == 'U.S.S.R.':
        return 'RUS'
    return coco.convert(country_name, to='ISO3', not_found=None)


def tolerant_region_conversion(region_name: str) -> str:
    """
    Converts a region name to its ISO3 equivalent, returning None if not found.
    """
    code = {"Africa": "AFR",
            "Asia": "ASI",
            "Europe": "EUR",
            "North America": "AMN",
            "Oceania": "OCE",
            "South America": "AMS"}
    if region_name in code.keys():
        return code[region_name]
    
    #Check if the region name is already in ISO3 format
    region_name = region_name.strip()
    if len(region_name) == 3:
        return region_name
    return coco.convert(region_name, to='ISO3', not_found=None)