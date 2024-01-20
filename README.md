# Creators:
Matthew, Jerry, Becky

# Preview:
This app allows users to upload poster images and QR codes of events and download an iCal file (they are used to save events on calendar apps).

## Upload an Image:

![Alt text](/demoimages/image.png)

## Download the File
![Alt text](/demoimages/image-1.png)

## Get an iCal file with relevant event and date
![Alt text](/demoimages/image-2.png)

# Production Setup
## Packages to install for Ubuntu:
```bash
sudo apt-get update
sudo apt-get upgrade
```

### Install Docker
Now we install the Docker https://docs.docker.com/engine/install/ubuntu/
```bash
# Add Docker's official GPG key:
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl start docker
```

After Docker is installed, navigate to project's root folder.
```bash
sudo docker compose up -d
```

To Do:
- Add env variables to docker setup for prod vs dev

### Install libzbar0
```bash
sudo apt-get install libzbar0
```
