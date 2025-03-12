
# FROM python:3.9-slim

# WORKDIR /app

# # Install system dependencies (if needed)
# RUN apt-get update && apt-get install -y \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY frontend/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy frontend code
# COPY ./frontend/ /app/

# # Expose the port
# EXPOSE 8501

# # Set the entrypoint and command
# ENTRYPOINT ["streamlit", "run"]
# CMD ["streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]





FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend code
COPY backend/frontend /app/

# Expose the port
EXPOSE 8501

# Set the entrypoint and command
ENTRYPOINT ["streamlit", "run"]
CMD ["streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]