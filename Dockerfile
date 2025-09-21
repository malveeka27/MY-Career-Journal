# PYTHON IMAGE SETTING
FROM python:3.11-slim

WORKDIR /app


RUN pip install --upgrade pip

# COPYING REQUIREMENTS.TXT AND SETTING UP DEPENDENCIES
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY FILES
COPY . .

# EXPOSE PORT FOR STREAMLIT
EXPOSE 8080

# RUNNING STREAMLIT
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]



