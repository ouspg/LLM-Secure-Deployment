# Frontend Dockerfile


# First build the React app
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

# Setup NGINX as a proxy server to serve the app
FROM nginx:latest as prod

# Copy required files to the NGINX container
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY cert.pem /etc/nginx/ssl/cert.pem
COPY key.pem /etc/nginx/ssl/key.pem

EXPOSE 443

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]