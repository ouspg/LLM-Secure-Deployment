# Frontend Dockerfile
# official base img
FROM node:latest as build

WORKDIR /app

# Add /app/node_modules/.bin to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# Install Dependencies
COPY package.json ./
COPY package-lock.json ./

#RUN npm install axios 
#should work without above command
RUN npm install 
RUN npm install react-scripts@3.4.1 -g

COPY . /app/

# Build production
RUN npm run build
RUN npm install -g serve

# Start app on selected port (3006)
CMD serve -s build -l 3006