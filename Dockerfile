FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .

RUN mkdir -p data output

# BOT_TOKEN is read from the environment at runtime - pass it with `docker run -e`
# or a compose `environment:` block, never baked into the image.
CMD ["python", "bot.py"]
