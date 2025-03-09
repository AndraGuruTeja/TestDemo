FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend code
COPY ./frontend/ /app/

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]