"""
Google CHAOS Translator

This script demonstrates the use of the Google Translate API to perform 
asynchronous translation chains. It uses the asyncio library for concurrent 
execution and the googletrans library for translation.

Version: 0.95-A
"""
 
import asyncio
import json

from translate import translation_chain
import checkpoint
async def main(iterations, src_lang, file_path, resume_path=None):
    if resume_path:
        # Resume from checkpoint
        with open(resume_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            current_text = data["text"]
            path = data["path"]
            completed = data["iteration"]
            remaining = iterations - completed
            
            if remaining <= 0:
                print("No iterations remaining.")
                return

            result, new_path = await translation_chain(
                current_text, 
                src_lang, 
                remaining, 
                initial_path=path
            )
            full_path = path + new_path
    else:
        # Start normally
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        result, full_path = await translation_chain(text, src_lang, iterations)
    
    print("\n" + "="*50)
    print(f"Iterations: {iterations}")
    print(f"Original text: {text[:50]}...") # Only display the first 50 characters 
    print(f"Final result: \n{result}")
    print(f"Langugage path: {' → '.join(path)}")
    print("="*50)
 
if __name__ == "__main__":
    import argparse 
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',  '--iterations', type=int, required=True, help="Number of iterations")
    parser.add_argument('-s',  '--src-lang', type=str, required=True, help="Source language")
    parser.add_argument('-f',  '--file', type=str, required=True, help="Input file path")
    parser.add_argument('-o',  '--output', type=str, help="Output file path")
    parser.add_argument("--resume", type=str, help="Path to checkpoint file for resuming")
    args = parser.parse_args() 
    
    try:
        asyncio.run(main(
            args.iterations, 
            args.src_lang, 
            args.file, 
            resume_path=args.resume
        ))
    except KeyboardInterrupt:
        print("Process interrupted.")
        print(f"Checkpoint saved to: translation_checkpoint.json")