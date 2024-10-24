# Open the docker app and run the following commands:
# TO BUILD THE IMAGE FOR YOUR PLATFORM: 
#
# docker build -t REPO-NAME .
#
# TU RUN THE DOCKER CONTAINER: 
#
# docker run -p PORT:PORT REPO-NAME
#
#
# TO PUSH THE IMAGE TO DOCKER HUB:
# docker login
#
# docker tag REPO-NAME:latest ACCOUNT-NAME/REPO-NAME:latest
#
# docker push ACCOUNT-NAME/REPO-NAME:latest
#
#
#
# TO BUILD THE IMAGE FOR MULTIPLE PLATFORMS:
# First create the builder for the multiplatform image if not exixt.
# Use the following command to see if exit:
#
# docker buildx ls
#
# If not create and activate it with:
#
# docker buildx create --name BUILDER-NAME
#
# docker buildx use BUILDER-NAME
#
# docker buildx inspect --bootstrap
#
# The create on docker hub the repository if you want to deploy if not skip
# Suppose you want to deploy and the repo is colled REPO-NAME Now you can build the image with the following command:
# Remember the point at the end in the row below --push \
#
# docker buildx build --platform linux/amd64,linux/arm64 -t ACCOUNT-NAME/REPO-NAME:latest --push .
#
# If you want it locally instead (maybe):
#
# docker buildx build --platform linux/amd64,linux/arm64 -t REPO-NAME --pull .
#
#

FROM python:3.12.7

# Set the working directory
WORKDIR /gem_digest_bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and dependencies
RUN pip install --no-cache-dir playwright && \
    playwright install && \
    playwright install-deps

COPY ./src .

# ENTRYPOINT [ "bash" ]
CMD ["python", "-u", "src/main.py"]