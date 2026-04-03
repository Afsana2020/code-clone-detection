FROM python:3.14-slim

WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose the port Render expects
EXPOSE 10000

# Run the app with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]