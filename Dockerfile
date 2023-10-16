# TODO: update base image to current recommended version of node
# https://nodejs.org/en/
FROM node:16

# Docker Node image includes non-root user node
# we can run application container as "node" instead of "root"
# it's recommended security practice to avoid running containers as root and restrict capabilites

# specifying permissios of the node user
# creating /node_modules and /app so we can make sure they have the permissions we want
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app /home/node/app
# additional resource on utility of RUN instructions: https://www.digitalocean.com/community/tutorials/building-optimized-containers-for-kubernetes#managing-container-layers

# set working directory of the application
WORKDIR /home/node/app
# copy package.json and package-lock.json into container
# running COPY prior to npm install let's us take advantage of Docker caching
COPY package*.json ./
# COPY local_packages ./

# switch user before running npm intall to make sure all application files owned by node instead of root
# commented out next line bc was getting EACCESS errors
# USER node
RUN npm install 
# TODO: do I need to RUN a separate npm install multer in order to install multer?

# install python dependencies
RUN apt-get install python3-pip

RUN pip3 install biopython matplotlib

# copy application code with appropriate permissions to the application directory on the container
COPY --chown=node:node . .

# expose the appropriate port (doesn't publish, but lets you know which port to publish at runtime)
# this should match the port specified in the bin/www file
EXPOSE 8000

# start the application
CMD [ "npm", "run", "dev" ]
