FROM nginx:alpine

LABEL maintainer="Ravza_Ozkara"
LABEL description="Nginx server for TODO APP"
LABEL version="1.0"

# Copy static files
COPY index.html /usr/share/nginx/html/

# Set proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html/*

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]