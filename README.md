# NIH Containerization Project - VASP Example

## Purpose:

Overall: Build a web server that is responsive to HTTP requests in order to run bioinformatics software. \
VASP Example: Create an example web app that runs a bioinformatics command-line executable code and produces 3D visualizations of input and output files. In this example, the executable code is a program called VASP that takes .SURF files as inputs, performs an operation on these 3D models (intersection, union, or difference), and produces an output .SURF file. This project will then be made into a Docker container so other researchers can use it more easily, and it can be used as an example for containerization of bioinformatics software.

## Goals:

- Containerize bioinformatics software
- Create a release system to push well-scripted software to the cloud and make the software callable by web requests
  - This would make the system easily scalable
- Use (AWS) credentials to log into web app in order to pay for/allocate CPU time
  - Takes this responsibility away from the authoring lab

## Install and Run (Locally)

You must have node.js running on your machine. Once you have cloned this project you can run `npm install` to install all the packages for this project. Then running `npm run dev` will run the dev version of this code, which will run this project with nodemon. Nodemon auto-restarts the node server every time you make a change to a file. Very helpful when you are writing and testing code.

After running the dev version of the code, go to "localhost:8000" in your browser to see the frontend of the project.

## Testing and Running (social sandbox server)

The formal iteration of this project is deployed at socialsandbox.xyz. To access this server, ssh into socialsandbox.xyz by typing "ssh abc123@socialsandbox.xyz" into your command line (where abc123 is your username for the server). Then sign in with your password. This project is cloned in the /srv folder, which you can access after logging in by running "cd ../../srv/containerization".

You should avoid modifying code from the server. You should only perform "git pull" from the server to update the server version of the project from code that has already been tested on your local machine. Note that in order to perform a git pull on the server, you will need to use sudo.

On the server, the Node app is up and running using pm2. See the "Useful Resources" section for more inforamtion about using pm2.

## Current Routes

### GET ‘/’

This route retrieves the home page. Currently, the home page just has buttons for:

- Running an example hardcoded vasp run using assumed inputs (GET ‘/run’)
  ./vasp -csg test1.SURF test2.SURF I output.SURF 0.5
- Redirecting to a test page (GET ‘/test’)
- Uploading two files (POST ‘/files’)
- Uploading two files and running vasp with those files (POST ‘/vasp’)

### -- GET ‘/test’

This route retrieves the test page, which is just a page with a button to return to the home page.

- Adyn created this simple route to test if routes were working on the server instead of using console.log to test if a route has been entered (because console.log statements aren’t showing up)
- As of 6/7, the routes AREN’T working, and I don’t know why. They are working on my local, which makes me think something is going wrong with the server.

### GET ‘/vasp’

This route performs a hardcoded vasp command on the server.

- Command that is run: ./vasp -csg test1.SURF test2.SURF I output.SURF 0.5
- Assumes test1.SURF, and test2.SURF are all already uploaded in the /uploads folder
- Assumes vasp executable is contained in the parent folder of the present working directory
- The other arguments are I for intersection, output.SURF for the name of the output file, and 0.5 for the resolution

### -- POST ‘/files’

This route takes two input files from the index page and uploads them into the /uploads folder using multer.

### POST ‘/vasp’

This route takes two input files from the index page, uploads them into the /uploads folder using multer, and then runs vasp using these files.
Requires .SURF files. If a file type other than .SURF is uploaded, it will give whatever error occurs when vasp is run using incorrect input files.

- All variables for vasp are taken is as arguments in req.body (output file name, operation, and resolution).
- All error checking is done on the frontend in index.pug
  - input files must be of type .SURF
  - operation must be 'I', 'U', or 'D'
  - resolution must be a number between 0.25 and 2

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
