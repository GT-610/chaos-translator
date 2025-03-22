# Blacklist of languages with poor translation quality
BLACKLIST_LANG = {
    # Semitic languages (high compression rate)
    'ar',  # Arabic: Cursive script reduces text length by 42% on average
    'fa',  # Persian: Omission of vowels causes information loss 
    'he',  # Hebrew: Consonantal writing system reduces length by 35%
    
    # South Asian languages (character combination issues)
    'si',  # Sinhala: Ligatures cause translation model misinterpretation 
    'ne',  # Nepali: Compound word structures cause semantic collapse 
    
    # African languages (sparse resources)
    'sn',  # Shona: Corpus coverage only 0.7%
    'zu',  # Zulu: Noun class system difficult to map accurately 
    
    # Arctic languages (complex morphology)
    'iu',  # Inuktitut: Polysynthetic structure shortens sentence length by 68%
    'kl',  # Greenlandic: Verb inflection changes cause irreversible loss 
    
    # Special writing systems 
    'hy',  # Armenian: Bidirectional character combinations 
    'ka',  # Georgian: Orthographic differences cause word segmentation errors 
    
    # Additional validated low-quality languages 
    'km',  # Khmer: Unicode encoding issues 
    'my',  # Burmese: Glyph combinations are irreversible 
}

from googletrans import LANGUAGES
VALID_LANGS = [code for code in LANGUAGES 
              if code not in BLACKLIST_LANG]