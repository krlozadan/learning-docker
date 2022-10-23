# Specify base image
FROM node:14-alpine

# Change directory
WORKDIR /usr/app

# Copy dependencies file
COPY package.json .

# Install dependencies
RUN npm install

# Copy 
COPY src src

CMD ["npm", "start"]