import pytest
from PROJECTROOT import translation
from PROJECTROOT import utc_to_regular
from PROJECTROOT import input_check


print(input_check('Москва', False))
def test_f():
    assert translation('Новоколочанск') == ('Novokolochansk')
    assert translation('Москва') == ("Moscow")
    assert translation('Казань') == ("Kazan")
    assert input_check('2315221', False) == (False, '2315221')
    assert input_check('Moscow', True) == (True, 'Moscow')
    assert input_check('Москва', False) == (True , 'Moscow')
    assert input_check("Москва", True) == (False, 'Москва')
    assert utc_to_regular('1703004885') == "19:54:45"
    assert utc_to_regular('0') == '03:00:00'
    
    

                    
