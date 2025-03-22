import json

def save(text, path, iteration, checkpoint_file):
    try:
        data = {
            "text": text,
            "path": path,
            "iteration": iteration
        }
        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Checkpoint saved to {checkpoint_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to save checkpoint: {str(e)}")
        return False