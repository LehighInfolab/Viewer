# NIH Containerization Project - Example Template

## [<span style="color:blue">Web Server </span>](https://viewer-backend-dev-sqrlv2g2yq-uc.a.run.app/)

## Purpose:

Overall: Build a web server that is responsive to HTTP requests in order to run bioinformatics software. \
Example: Create an example web app that runs a bioinformatics command-line executable code and produces 3D visualizations of input and output files. This project will then be made into a Docker container so other researchers can use it more easily, and it can be used as an example for containerization of bioinformatics software.

## Goals:

- Containerize bioinformatics software
- Create a release system to push well-scripted software to the cloud and make the software callable by web requests
  - This would make the system easily scalable
- Use Google Cloud Run to run server and compute
  - Takes this responsibility away from the authoring lab

## Install and Run (Locally)

You must have node.js running on your machine. Once you have cloned this project you can run `npm install` to install all the packages for this project. Then running `npm run dev` will run the dev version of this code, which will run this project with nodemon. Nodemon auto-restarts the node server every time you make a change to a file. Very helpful when you are writing and testing code.

After running the dev version of the code, go to "localhost:8000" in your browser to see the frontend of the project.

## Testing and Running ()

You can download the container and test on Google Cloud or on docker locally. Follow docker-container tutorial for these steps.

## Useful Resources

Overview of pm2 and useful commands:

- https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/

Explanation of exec/spawn to execute shell commands:

- https://stackabuse.com/executing-shell-commands-with-node-js
- https://nodejs.org/api/child_process.html

Explanation of multer (middleware to upload files):

- https://www.npmjs.com/package/multer
- https://www.bacancytechnology.com/blog/file-upload-using-multer-with-nodejs-and-express

Docker resources:
Docker is a containerization software. To create a Docker container, all you have to do is create a Dockerfile in your root directory of your project. A Dockerfile is a simple text file with commands for how Docker will create an image for your container. A Docker image is essentially a blueprint for your container. The image becomes a container when it is activated.

- https://www.docker.com/
- make an account, download Docker Desktop (or do the tutorial on the cloud) and follow the getting-started tutorial, which I believe is prompted when you download Docker Desktop: https://docs.microsoft.com/en-us/visualstudio/docker/tutorials/docker-tutorial

To Dockerize your project:
overview: https://blog.iron.io/how-to-create-a-docker-container/#1

1. Create a Dockerfile

- https://nodejs.org/en/docs/guides/nodejs-docker-webapp/
- https://kapeli.com/cheat_sheets/Dockerfile.docset/Contents/Resources/Documents/index

2. Use "docker build" to use your Dockerfile to create a Docker image

- https://www.techrepublic.com/article/how-to-create-your-own-docker-image/
- https://docs.docker.com/engine/reference/commandline/build/

3. If applicable, push your image to the Docker Hub so it can be shared with others.

- https://techtutorialsite.com/docker-push-images-to-dockerhub/

5. Activate your Docker image to create a running container

- https://blog.iron.io/how-to-create-a-docker-container/

OTHER POSSIBLY USEFUL LINKS
https://codeburst.io/dockerize-deploy-1cfc4f0e7c72 \
https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md \
https://medium.com/codebase/using-aws-s3-buckets-in-a-nodejs-app-74da2fc547a6 \
https://docs.docker.com/engine/reference/builder/ \
