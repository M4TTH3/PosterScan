FROM nginx:latest

# Remove default nginx server
RUN rm /etc/nginx/conf.d/*

# Replace with the new nginx conf
COPY nginx.conf /etc/nginx/nginx.conf
