import codecs
from collections import defaultdict

from nexus import NexusWriter, NexusReader

from .CognateParser import CognateParser

ASCERTAINMENT_CHOICES = (
    'none',
    'overall',
    'perword',
)

class Record(object):
    def __init__(self, language=None, word=None, item=None, annotation=None, loan=None, cognate=None):
        self.language = language
        self.word = word
        self.item = item
        self.annotation = annotation
        self.loan = loan
        self.cognate = cognate
    
    @property
    def is_loan(self):
        if self.loan is None:
            return False
        elif self.loan in (False, ""):
            return False
        elif self.loan is True:
            return True
        else:
            return True
    

class NexusMaker(object):
    
    UNIQUE_IDENTIFIER = "-u_"
    
    def __init__(self, data, cogparser=CognateParser(strict=True, uniques=True), remove_loans=True):
        self.data = [self._check(r) for r in data]
        
        self.cogparser = cogparser
        
        # loan words
        self.remove_loans = remove_loans
        if self.remove_loans:
            self.data = [r for r in data if not r.is_loan]
        
    def _check(self, record):
        """Checks that all records are instances of `Record`"""
        if not isinstance(record, Record):
            raise ValueError('records must be of type Record')
        return record
    
    def _is_missing_for_word(self, language, word):
        """Returns True if the given `language` has no cognates for `word`"""
        for cog in [c for c in self.cognates if c[0] == word]:
            if language in self.cognates[cog]:
                return False
        return True
        
    @property
    def languages(self):
        if not hasattr(self, '_languages'):
            self._languages = {r.language for r in self.data}
        return self._languages
        
    @property
    def words(self):
        if not hasattr(self, '_words'):
            self._words = {r.word for r in self.data}
        return self._words
    
    @property
    def cognates(self):
        if not hasattr(self, '_words'):
            self._cognates = {}
            for rec in self.data:
                if self.remove_loans and rec.is_loan:
                    raise ValueError("%r is a loan word!")
                
                for cog in self.cogparser.parse_cognate(rec.cognate):
                    coglabel = (rec.word, cog)
                    self._cognates[coglabel] = self._cognates.get(coglabel, set())
                    self._cognates[coglabel].add(rec.language)
        return self._cognates
    
    def make(self):
        nex = NexusWriter()
        for cog in self.cognates:
            if self.UNIQUE_IDENTIFIER in cog:
                assert len(self.cognates[cog]) == 1
            else:
                assert len(self.cognates[cog]) >= 1, "%s = %r" % (cog, self.cognates[cog])
            
            coglabel = "_".join(cog)
            for lang in self.languages:
                if lang in self.cognates[cog]:
                    nex.add(lang, coglabel, '1')
                elif self._is_missing_for_word(lang, cog[0]):
                    nex.add(lang, coglabel, '?')
                else:
                    nex.add(lang, coglabel, '0')
        
        nex = self._add_ascertainment(nex)  # handle ascertainment
        return nex
    
    def _add_ascertainment(self, nex):
        # subclass this to extend
        return nex
    
    def write(self, nex=None, filename=None):
        if nex is None:
            nex = self.make()
        
        if filename is None:
            return nex.write(charblock=True)
        else:
            return nex.write_to_file(filename=filename, charblock=True)
        
        
        
class NexusMakerAscertained(NexusMaker):
    
    OVERALL_ASCERTAINMENT_LABEL = '_ascertainment_0'
    
    def _add_ascertainment(self, nex):
        """Adds an overall ascertainment character"""
        if self.OVERALL_ASCERTAINMENT_LABEL in nex.data:
            raise ValueError('Duplicate ascertainment key %s!' % self.OVERALL_ASCERTAINMENT_LABEL)
            
        for lang in self.languages:
            nex.add(lang, self.OVERALL_ASCERTAINMENT_LABEL, '0')
        return nex


class NexusMakerAscertainedWords(NexusMaker):
    
    def _add_ascertainment(self, nex):
        """Adds an ascertainment character per word"""
        for word in self.words:
            coglabel = '%s_0' % word
            if coglabel in nex.data:
                raise ValueError('Duplicate ascertainment key %s!' % coglabel)
            
            for lang in self.languages:
                if self._is_missing_for_word(lang, word):
                    nex.add(lang, coglabel, '?')
                else:
                    nex.add(lang, coglabel, '0')
        return nex
    
    def _get_characters(self, nex, delimiter="_"):
        """Find all characters"""
        chars = defaultdict(list)
        for site_id, label in enumerate(sorted(nex.data.keys())):
            if delimiter in label:
                word, cogid = label.rsplit(delimiter, 1)
            else:
                raise ValueError("No delimiter %s in %s" % (delimiter, label))
            chars[word].append(site_id)
        return chars

    def _is_sequential(self, siteids):
        return sorted(siteids) == list(range(min(siteids), max(siteids)+1))

    def create_assumptions(self, nex):
        chars = self._get_characters(nex)
        buffer = []
        buffer.append("begin assumptions;")
        for char in sorted(chars):
            siteids = sorted(chars[char])
            # increment by one as these are siteids not character positions
            siteids = [s+1 for s in siteids]
            assert self._is_sequential(siteids), 'char is not sequential %s' % char
            if min(siteids) == max(siteids):
                out = "\tcharset %s = %d;" % (char, min(siteids))
            else:
                out = "\tcharset %s = %d-%d;" % (char, min(siteids), max(siteids))
            buffer.append(out)
        buffer.append("end;")
        return buffer

    def write(self, nex=None, filename=None):
        if nex is None:
            nex = self.make()
        
        if filename is None:
            return nex.write(charblock=True) + "\n\n" + "\n".join(self.create_assumptions(nex))
        else:  # pragma: no cover
            nex.write_to_file(filename=filename, charblock=True)
            with open(filename, 'a', encoding='utf8') as handle:
                handle.write("\n")
                for line in self.create_assumptions(nex):
                    handle.write(line + "\n")
                handle.write("\n")
            return True
