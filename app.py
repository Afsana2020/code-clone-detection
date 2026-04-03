from flask import Flask, request, jsonify, render_template
import torch
import torch.nn.functional as F
from transformers import RobertaTokenizer
import json
import os
import warnings
warnings.filterwarnings('ignore')

from model import LightweightModel

app = Flask(__name__)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

try:
    model = LightweightModel()
    model.load_state_dict(torch.load("lightweight_model.pt", map_location=device, weights_only=False))
    model.to(device)
    model.eval()
    print(" Model loaded successfully")
except Exception as e:
    print(f" Error loading model: {e}")
    print("Trying alternative loading method...")
    try:
        model = LightweightModel()
        # Load to CPU first then move to device
        state_dict = torch.load("lightweight_model.pt", map_location='cpu', weights_only=False)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        print(" Model loaded with alternative method")
    except Exception as e2:
        print(f" Failed to load model: {e2}")
        model = None

# Load tokenizer
try:
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
    print(" Tokenizer loaded")
except Exception as e:
    print(f" Tokenizer error: {e}")
    try:
        tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base", local_files_only=True)
        print(" Tokenizer loaded (local)")
    except:
        tokenizer = None
        print(" Failed to load tokenizer")

# Load threshold
try:
    with open("config.json", "r") as f:
        config = json.load(f)
    THRESHOLD = config.get("best_threshold", 0.54)
except:
    THRESHOLD = 0.54
    print(f" Using default threshold: {THRESHOLD}")

print(f" Threshold: {THRESHOLD}")

def get_embedding(code):
    if model is None or tokenizer is None:
        return None
    inputs = tokenizer(
        code,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)

    with torch.no_grad():
        embedding = model.encode(input_ids, attention_mask)
    return embedding

@app.route('/')
def home():
    return render_template('index.html', threshold=THRESHOLD)

@app.route('/compare', methods=['POST'])
def compare():
    try:
        data = request.json
        emb_a = get_embedding(data['code_a'])
        emb_b = get_embedding(data['code_b'])
        
        if emb_a is None or emb_b is None:
            return jsonify({'error': 'Model not properly loaded'}), 500

        similarity = F.cosine_similarity(emb_a, emb_b).item()
        distance = torch.dist(emb_a, emb_b, p=2).item()
        is_clone = similarity >= THRESHOLD

  
        emb_a_preview = [f"{x:.4f}" for x in emb_a[0, :20].detach().cpu().numpy()]
        emb_b_preview = [f"{x:.4f}" for x in emb_b[0, :20].detach().cpu().numpy()]

        return jsonify({
            'similarity': similarity,
            'similarity_percent': round(similarity * 100, 1),
            'distance': distance,
            'is_clone': is_clone,
            'threshold': THRESHOLD,
            'emb_a_preview': emb_a_preview,
            'emb_b_preview': emb_b_preview
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    print("\n" + "="*50)
    print(" Server ready at http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
