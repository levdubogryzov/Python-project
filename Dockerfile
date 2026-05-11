FROM manimcommunity/manim:latest
USER root
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir pydantic rich
COPY . .
RUN mkdir -p data media profiling && chmod -R 777 /app
CMD ["python", "main.py"]