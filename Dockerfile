# base image
FROM mysql

# Add a database
ENV MYSQL_DATABASE ad2dispatch
# Add root password
ENV MYSQL_ROOT_PASSWORD p@ssw0rd

# Add a user
ENV MYSQL_USER ad2dispatch
# Add the password
ENV MYSQL_PASSWORD password

RUN mysql_ssl_rsa_setup