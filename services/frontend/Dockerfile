# Frontend Dockerfile - Simple approach using pre-built files
FROM nginx:1.25-alpine

# Remove default nginx configuration to prevent conflicts
RUN rm -f /etc/nginx/conf.d/default.conf

# Copy pre-built app to nginx
COPY dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Verify files were copied correctly and set permissions
RUN ls -la /usr/share/nginx/html/ && \
    ls -la /usr/share/nginx/html/js/ && \
    ls -la /usr/share/nginx/html/css/ && \
    chmod -R 755 /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]