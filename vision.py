model = None
processor = None

def load_model(model_path="./models"):
    """Load vision model. Returns False if model not available."""
    global model, processor
    try:
        from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
        import torch

        processor = AutoProcessor.from_pretrained(model_path, local_files_only=True)
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            local_files_only=True
        )
        model.eval()
        print("Vision model loaded successfully")
        return True
    except Exception as e:
        print(f"Vision model not available: {e}")
        print("Continuing without vision capabilities...")
        return False
