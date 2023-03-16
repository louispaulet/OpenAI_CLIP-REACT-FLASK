# Use the official Node.js base image
FROM node:14

# Set the working directory
WORKDIR /app

# Create the React app
RUN npx create-react-app . --use-npm

# Copy package.json and package-lock.json
COPY package*.json ./

# Install additional dependencies
RUN npm install axios

# Copy the source code
COPY src ./src

# Build the app
RUN npm run build

# Use the official Nginx base image
FROM nginx:1.21

# Copy the build artifacts to the Nginx html directory
COPY --from=0 /app/build /usr/share/nginx/html

# Expose the default Nginx port
EXPOSE 80
