# Specify base image
FROM node:14-alpine

# Change directory
WORKDIR /usr/app

# Copy application files
COPY ./ ./

# Install dependencies
RUN npm install

CMD ["npm", "start"]