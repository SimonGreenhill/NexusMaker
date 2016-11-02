import unittest

from nexusmaker import Record

class TestRecord(unittest.TestCase):
    
    def test_simple(self):
        r = Record(language='English', word='Hand', item='hand', annotation='?')
        assert r.language == 'English'
        assert r.word == 'Hand'
        assert r.item == 'hand'
        assert r.annotation == '?'
        assert r.loan == None
        assert r.cognate == None
    
    def test_is_loan(self):
        assert not Record(loan="").is_loan
        assert not Record(loan=None).is_loan
        
        assert Record(loan="L").is_loan
        assert Record(loan="English").is_loan
        assert Record(loan=True).is_loan
    
        
if __name__ == '__main__':
    unittest.main()


