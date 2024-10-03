FROM python:3.12.7

# Set the working directory
WORKDIR /gem_digest_bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and dependencies
RUN pip install --no-cache-dir playwright && \
    playwright install && \
    playwright install-deps

COPY . .

# ENTRYPOINT [ "bash" ]
CMD ["python", "-u", "src/main.py"]