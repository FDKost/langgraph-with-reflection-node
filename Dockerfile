# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port if needed (not used in this CLI example)
# EXPOSE 8000

# Set environment variable for OpenAI key
# In production, pass the key via environment variable
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Run the application
CMD ["python", "main.py", "Explain to a student the difference between tool and resource in MCP."]
