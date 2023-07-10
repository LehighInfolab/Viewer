**Docker Tutorial**

1. Installing Docker ……………………………………………………………….
2. Pulling Repository/Image ……………………………………………………..
3. Running Container …………………………………………………………….
4. Building a Docker Image……………………………………………………..
5. Troubleshooting Problems & Solutions ……………………………………. 

![](RackMultipart20230710-1-v88ajy_html_c7410f47001e161d.png)

**Installing Docker**

Go to [https://hub.docker.com](https://hub.docker.com/) and login to your account.

- If you don't already have a Docker account, you will need to create one

- It's free to create, select the free plan ↓

![](RackMultipart20230710-1-v88ajy_html_7f76b5942f153be2.png)

- Verify your email
- Download **Docker Desktop Application** ↓

![](RackMultipart20230710-1-v88ajy_html_dd69121bc5fcf5c8.png)

    - Verify Docker installed by running the command\> docker
      - Should result in a list of docker help commands
  - Open the Docker Desktop Application
    - Docker will prompt you to allow privileges, allow it
    - Accept the service agreement
  - Sign In on the Docker Desktop Application ↓

![](RackMultipart20230710-1-v88ajy_html_4340fad585cca53b.png)

**Pulling Repository/Image**

Go to docker repository:

[https://hub.docker.com/repository/docker/jtamwaffle/visual/general](https://hub.docker.com/repository/docker/jtamwaffle/visual/general)

Copy the command ↓ ![](RackMultipart20230710-1-v88ajy_html_ab03ffd7883c03ea.png)

Open a terminal and enter the command\> docker pull jtamwaffle/visual

- You should see this when its finished ↓
 ![](RackMultipart20230710-1-v88ajy_html_1c8a3459223b75d.png)
- To check if the repository pulled, enter the command\> docker images
You should see the following ↓
 ![](RackMultipart20230710-1-v88ajy_html_4234b0bffa428571.png)

**Running Container**

Now that the image is pulled, you can run it through the terminal or you can run it through the Docker Desktop Application. I will show how to run it through the Docker Desktop Application first:

- In the desktop application, click the **Images** tab on the left ↓
 ![](RackMultipart20230710-1-v88ajy_html_7e89c2683eab4495.png)
- Then, click **run** for the image you want to create a container for ↓
 ![](RackMultipart20230710-1-v88ajy_html_6e4aba8f413128b0.png)
 This window should pop up to run a new container, go to **Optional Settings** ↓
 ![](RackMultipart20230710-1-v88ajy_html_d8afb794c793d812.png)
- Go to **Ports -\> Host Port** and enter the port number to run on your local machine. I chose port 8080 for this tutorial ↓
 ![](RackMultipart20230710-1-v88ajy_html_28283d1e5b71651c.png)
  - This port number is the local host your machine will use to run and view the container
  - The default port the container will use is 8000
- Then, **run** the container ↓
 ![](RackMultipart20230710-1-v88ajy_html_1fc16d70726a51da.png)
- You should be taken to the **Container** tab and see the following ↓
 ![](RackMultipart20230710-1-v88ajy_html_d01d2d35fb702506.png)
  - You can also validate the container is running in the terminal by using the command\> docker ps
    - You should see the following

![](RackMultipart20230710-1-v88ajy_html_714f1cc4e0eed2ac.png)

To run the application through the terminal

- Use the command\> docker run -d -p \<local port\>:8000 \<image ID\>
  - If you do not know the image ID
    - Go to the **Images** tab in the desktop application
    - Under the image you need the ID for is the image ID ↓

![](RackMultipart20230710-1-v88ajy_html_4691ce9f2a19be54.png)

- To view the container, go to [http://localhost](http://localhost/):\<local port\>
  - If you used the port number 8080, go to [http://localhost:8080](http://localhost:8080/)
  - You should see the running container ↓ ![](RackMultipart20230710-1-v88ajy_html_6a151a0ee0992ebe.png)

When you're done using the container, you should stop the container. This can be done either by using the Docker Desktop Application or through the terminal.

- Using the desktop application, under the **Container** tab, press the stop button at the top of the page for the container you want to stop ↓
 ![](RackMultipart20230710-1-v88ajy_html_6bba700542ebf623.png)
- Using the terminal, enter the command\> docker stop \<container ID\>
  - If you do not know the container ID, enter the command\> docker ps

- The container ID will be listed in the first column ↓

![](RackMultipart20230710-1-v88ajy_html_d0ce38bb37bf04f0.png)

**Building a Docker Image**

This will cover two ways to build a docker image, the first method builds a docker image from the git repository. The second method builds the docker image from a pre-existing docker image, like a copy of the docker image.

Building a Docker Image from Git Repository

- Go to the location where you locally stored the git repository

- Within the git repo is an already made Dockerfile that will be used for building the docker image.

- To build the docker image, use the command\> docker build -t \<tagname\> \<path\>

- For the tagname, I recommend using your username followed by the name for the docker image
  - Ex) anc224/visual:1.0
- Use '.' for the path to indicate that you are building the image from the current directory

![](RackMultipart20230710-1-v88ajy_html_d45e66a586e2ce06.png)

- Verify the docker image was created with the command\> docker images

Building a Docker Image from a Docker Image

- Create a Docker file
  - Command\> touch Dockerfile
    - Note that there are no file extensions
- Open Docker file
  - Command\> vim Dockerfile
    - Press 'i' to enter Insert Mode
- Type "FROM \<image name\>:latest"
 ![](RackMultipart20230710-1-v88ajy_html_dcfd0fb91c6b4271.png)
  - Save file and exit with ":x!"
- To build the docker image, use the command\> docker build -t \<tagname\> \<path\>

- For the tagname, I recommend using your username followed by the name for the docker image
  - Ex) anc224/visual:1.0
- Use '.' for the path to indicate that you are building the image from the current directory

![](RackMultipart20230710-1-v88ajy_html_b6e67e3948b3427a.png)

- Verify the docker image was created with the command\> docker images

![](RackMultipart20230710-1-v88ajy_html_4161b3c0a9cc578b.png)

  -

**Troubleshooting Problems & Solutions**

Command\> docker images

"Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?"

![](RackMultipart20230710-1-v88ajy_html_ed8b7605b39a7661.png)

- Solution: open the docker desktop application

Command\> docker build -t \<tagname\> \<path\>

"ERROR: [5/7] COPY local\_packages ./: failed to compute cache key: "/local\_packages" not found: not found"

![](RackMultipart20230710-1-v88ajy_html_53836c3c2b0989c8.png)