# Code Clone Detector

A code clone detection system using a customized lightweight contrastive learning approach with CodeBERT. Given two code snippets, it determines whether they solve the same programming problem by analyzing semantic similarity rather than just syntactic patterns.

## Use cases

- **Education** - Detect plagiarism in programming submissions
- **Code review** - Find duplicate logic across large codebases
- **IP protection** - Identify unauthorized code reuse in industry
- **Storage optimization** - Replace duplicate code with references, reducing repository size

##  Live Demo

**Link:** [https://huggingface.co/spaces/Afsana24/code-clone-detector](https://huggingface.co/spaces/Afsana24/code-clone-detector)

Paste two code snippets and see if they are clones (same problem, different implementation).

## Dataset

POJ-104 (104 categories of programming problems) : [https://huggingface.co/datasets/semeru/Code-Code-CloneDetection-POJ104](https://huggingface.co/datasets/semeru/Code-Code-CloneDetection-POJ104)


## How It Works

The model converts code snippets into an embedding space where:
- Same problem → embeddings are close (high cosine similarity)
  
![c1](https://github.com/user-attachments/assets/5053ae01-4e94-478f-a57b-1ca1d695a87b)
  
- Different problems → embeddings are far apart (low similarity)

![c2](https://github.com/user-attachments/assets/4a12c127-8190-4487-8588-e21a9527f7ea)


## Project Files

| File | Description | Purpose |
|------|-------------|---------|
| **app.py** | Flask web application | Main server, API endpoints, routes |
| **model.py** | Model architecture | LightweightModel class definition |
| **lightweight_model.pt** | Trained model weights | CodeBERT-base fine-tuned with customized lightweight contrastive learning |
| **config.json** | Configuration file | Threshold and model settings |
| **index.html** | Web interface | Frontend UI (HTML/CSS/JS) |
| **Dockerfile** | Container configuration | For Docker deployment |


### Local Setup

```bash
# Clone the repository
git clone https://github.com/Afsana2020/code-clone-detection-with-contrastive-learning.git
cd code-clone-detection-with-contrastive-learning

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open browser to http://localhost:5000


