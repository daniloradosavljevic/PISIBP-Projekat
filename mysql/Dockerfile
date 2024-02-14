# Use the official MySQL image from Docker Hub
FROM mysql:latest

# Set the environment variables
ENV MYSQL_ALLOW_EMPTY_PASSWORD=yes
ENV MYSQL_DATABASE=baze

# Copy the SQL file into the Docker container
COPY baze.sql /docker-entrypoint-initdb.d/

# Expose port 3306 to allow external connections to the database
EXPOSE 3306