# Use the official Nginx image from Docker Hub
FROM nginx:alpine

# Copy static files to the Nginx web directory
COPY index.html /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
