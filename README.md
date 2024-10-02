# GemDigest
GemDigest leverages the power of the Gemini API to summarize articles and PDFs, while collecting brief messages into personalized daily or weekly digests

### Build container
```bash
docker build -t gem_digest_bot .
```

### Use as dev container
```bash
docker run -v $(pwd):/home/GemDigest --env-file gem_digest.env -it -d --name gem_digest_dev gem_digest_bot bash
```

If the variables inside the `gem_digest.env` file change, restart the container to update the variables
```bash
docker restart gem_digest_dev
```

### Docker compose dev 
1. Build the container
    ```bash
    docker compose -f dev-docker-compose.yml build
    ```

1. Start the container:
    ```bash
    docker compose -f dev-docker-compose.yml up -d
    ```

To update environment variables in the dev-container stop the container:
```bash
docker compose -f dev-docker-compose down
```
And re-run steps 1 and 2

### Start the bot in the container
```bash
docker run --env-file gem_digest.env -d --name gem_digest_bot gem_digest_bot bash
```

### Using API keys
1. Copy `configs.env.example` to `configs.env`
2. Update the `configs.env` with your own API keys
3. Run the project with docker compose / docker

### Telegram api used:
    - pip3 install pyTelegramBotAPI
    - https://github.com/eternnoir/pyTelegramBotAPI

### Crawler used:
    - pip3 install crawl4ai
    - https://github.com/unclecode/crawl4ai?tab=readme-ov-file

### Gemini API used:
    - pip3 install google-generativeai

```bash
echo "export PYTHONDONTWRITEBYTECODE=1" >> ~/.bashrc
```