# Use the official Node.js image as a base
FROM node:current-alpine

# Set the working directory in the container
WORKDIR /frontend

# Copy the application files into the container
COPY . .

# Expose port 8080 for the application
EXPOSE 8080

# Install the necessary dependencies
RUN npm install
