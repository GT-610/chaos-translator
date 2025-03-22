from googletrans import Translator, LANGUAGES
import asyncio 
import random
import json

from blasklist import VALID_LANGS
import checkpoint

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
    checkpoint_file = f"checkpoint_{src_lang}_{iterations}.json"
    
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
            
            # API bug: Sometimes translation is the same as the original text
            if translated_text == current_text:
                try:
                    detected = translator.translator.detect(current_text)
                    current_src = detected.lang.lower()
                    print(f"⚠️ Translation failed, detected source language changed to {current_src}")
                    # Record the failed translation
                    path.append(f"{target_lang}({LANGUAGES[target_lang]}) - failed")
                except Exception as e:
                    print(f"⚠️ Language detection failed: {str(e)}")
                    # Keep current_src if detection fails
            else:
                # FIXME: Debug output, should be as an option in the future
                print(f"[Debug] Iteration {i+1}/{iterations} succeed.")
                print(f"├─ Origin language: {LANGUAGES.get(current_src,  'auto').upper()}({current_src})")
                print(f"├─ Target language: {LANGUAGES[target_lang].upper()}({target_lang})")
                print(f"├─ Input text: {current_text[:80]}...")
                print(f"└─ Output text: {translated_text[:80]}...\n")

                current_text = translated_text 
                current_src = target_lang  
                path.append(f"{target_lang}({LANGUAGES[target_lang]})")    

            # 无论成功或失败，都尝试保存检查点
            current_iteration = i + 1
            # checkpoint.save(
            #     current_text, 
            #     path, 
            #     current_iteration, 
            #     checkpoint_file
            # )
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
        except Exception as e:
            # 异常时也保存检查点
            checkpoint.save(
                current_text, 
                path, 
                current_iteration, 
                checkpoint_file
            )
            print(f"Iteration {i+1} failed: {str(e)}")
            return None, None 
       
    return current_text, path 