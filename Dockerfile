FROM python:3

# Set the working directory
WORKDIR /gem_digest_bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENTRYPOINT [ "bash" ]
CMD ["python", "-u", "src/main.py"]