import io
import pytest

from typing import Dict

from .passport import parse, validate


def test_parse():
    want = [
        {
            'ecl': 'gry',
            'pid': '860033327',
            'eyr': '2020',
            'hcl': '#fffffd',
            'byr': '1937',
            'iyr': '2017',
            'cid': '147',
            'hgt': '183cm',
        },
        {
            'iyr': '2013',
            'ecl': 'amb',
            'cid': '350',
            'eyr': '2023',
            'pid': '028048884',
            'hcl': '#cfa07d',
            'byr': '1929',
        },
        {
            'hcl': '#ae17e1',
            'iyr': '2013',
            'eyr': '2024',
            'ecl': 'brn',
            'pid': '760753108',
            'byr': '1931',
            'hgt': '179cm',
        },
        {
            'hcl': '#cfa07d',
            'eyr': '2025',
            'pid': '166559648',
            'iyr': '2011',
            'ecl': 'brn',
            'hgt': '59in',
        },
    ]
    got = list(parse(io.StringIO("""
        ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
        byr:1937 iyr:2017 cid:147 hgt:183cm
        
        iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
        hcl:#cfa07d byr:1929
        
        hcl:#ae17e1 iyr:2013
        eyr:2024
        ecl:brn pid:760753108 byr:1931
        hgt:179cm
        
        hcl:#cfa07d eyr:2025 pid:166559648
        iyr:2011 ecl:brn hgt:59in
    """)))
    assert want == got


@pytest.mark.parametrize(['passport', 'is_valid'], [
    pytest.param({
        'pid': '087499704',
        'hgt': '74in',
        'ecl': 'grn',
        'iyr': '2012',
        'eyr': '2030',
        'byr': '1980',
        'hcl': '#623a2f',
    }, True)
])
def test_validate(passport: Dict[str, str], is_valid: bool):
    assert validate(passport) == is_valid
