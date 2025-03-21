# Frontend Dockerfile
# official base img
FROM node:latest as build

WORKDIR /app

# Add /app/node_modules/.bin to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# Install Dependencies
COPY package.json ./
COPY package-lock.json ./

RUN npm install
RUN npm install -g serve
RUN npm install react-scripts@3.4.1 -g

COPY . /app

# Build production
RUN npm run build

# Start app on selected port (3006)
#CMD serve -s build -l 3006

# Setup NGINX as a proxy server to serve the app
FROM nginx:latest as prod

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY cert.pem /etc/nginx/ssl/cert.pem
COPY key.pem /etc/nginx/ssl/key.pem

EXPOSE 443

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]