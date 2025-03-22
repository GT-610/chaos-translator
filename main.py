"""
Google CHAOS Translator

This script demonstrates the use of the Google Translate API to perform 
asynchronous translation chains. It uses the asyncio library for concurrent 
execution and the googletrans library for translation.

Version: 0.90-A
"""
 
import asyncio 
import random 
from googletrans import Translator, LANGUAGES 
 
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

VALID_LANGS = [code for code in LANGUAGES 
              if code not in BLACKLIST_LANG and len(code) == 2]
 
class AsyncTranslator:
    def __init__(self, max_retries=3):
        self.translator  = Translator()
        self.retries  = max_retries 
        
    # Safe asynocious translation with exponential backoff
    async def safe_translate(self, text, src, dest):
        delay = 1.0 
        for attempt in range(self.retries): 
            try:
                async with self.translator  as trans:
                    result = await trans.translate(text,  src=src, dest=dest)
                    return result.text  
            except Exception as e:
                if attempt == self.retries  - 1:
                    raise 
                await asyncio.sleep(delay  * (2 ** attempt))
        return None 
 
 # Execute translation chain asynchronously
async def translation_chain(text, src_lang, iterations):
    current_text = text 
    path = []
    current_src = src_lang.lower()   # All languages should be lowercase
    
    for i in range(iterations):
        target_lang = src_lang if i == iterations-1 else random.choice(VALID_LANGS) 
        target_lang = target_lang.lower()   # Same as current_src
        
        try:
            translator = AsyncTranslator()
            # Use last translated information
            translated_text = await translator.safe_translate( 
                current_text, 
                src=current_src,
                dest=target_lang 
            )
            
            # FIXME: Debug output, should be as an option in the future
            print(f"[Debug] Iteration {i+1}/{iterations} succeed.")
            print(f"├─ Origin language: {LANGUAGES.get(current_src,  'auto').upper()}({current_src})")
            print(f"├─ Target language: {LANGUAGES[target_lang].upper()}({target_lang})")
            print(f"├─ Input text: {current_text[:80]}...")
            print(f"└─ Output text: {translated_text[:80]}...\n")
            
            current_text = translated_text 
            current_src = target_lang  # Update current source language for next iteration
            path.append(f"{target_lang}({LANGUAGES[target_lang]})")   # Record translation path
            
            await asyncio.sleep(random.uniform(0.5,  1.5))
            
        except Exception as e:
            print(f"Iteration {i+1} failed: {str(e)}")
            return None, None 
            
    return current_text, path 
 
async def main(iterations, src_lang, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().strip() 
    
    result, path = await translation_chain(text, src_lang, iterations)
    
    print("\n" + "="*50)
    print(f"Iterations: {iterations}")
    print(f"Original text: {text[:50]}...") # Only display the first 50 characters 
    print(f"Final result: {result}")
    print(f"Langugage path: {' → '.join(path)}")
    print("="*50)
 
if __name__ == "__main__":
    import argparse 
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',  '--iterations', type=int, required=True)
    parser.add_argument('-s',  '--src-lang', type=str, required=True)
    parser.add_argument('-f',  '--file', type=str, required=True)
    args = parser.parse_args() 
    
    asyncio.run(main(args.iterations,  args.src_lang,  args.file)) 