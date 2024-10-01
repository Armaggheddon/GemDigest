# GemDigest
GemDigest leverages the power of the Gemini API to summarize articles and PDFs, while collecting brief messages into personalized daily or weekly digests

### Build container
docker build -t gem_digest_bot .

### Use as dev container
```bash
docker run -v $(pwd):/home/GemDigest --env-file gem_digest.env -it -d --name gem_digest_dev gem_digest_bot bash
```

### Start the bot in the container
```bash
docker run --env-file gem_digest.env -d --name gem_digest_bot gem_digest_bot bash
```

### Telegram api used:
    - pip3 install pyTelegramBotAPI
    - https://github.com/eternnoir/pyTelegramBotAPI

### Crawler used:
    - pip3 install crawl4ai
    - https://github.com/unclecode/crawl4ai?tab=readme-ov-file