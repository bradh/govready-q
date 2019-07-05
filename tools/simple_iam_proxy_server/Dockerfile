# Build GocReady Simple IAM PROXY for IAM Single-Sign-On testing
#
# Build examples:
#   docker build --rm --tag govready/simple-iamproxy .
#   docker build --rm --tag govready/simple-iamproxy:local .
#
# Run examples:
#   docker run -it -p 80:8080 -d govready/simple-iamproxy
#   docker run -it -p 80:8080 -e BIND_PORT=8080 -d govready/simple-iamproxy

# Build on Docker's official CentOS 7 image.
FROM centos:7

# Expose the port docker uses for http by default.
EXPOSE 8080

# Put the Python source code here.
WORKDIR /usr/src/app

# Set up the locale. Lots of things depend on this.
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANGUAGE en_US:en

# Install required system packages.
RUN \
	yum -y install https://centos7.iuscommunity.org/ius-release.rpm \
	yum -y update \
	&& yum -y install \
	python36u python36u-devel.x86_64 python36u-pip gcc-c++.x86_64 \
	&& yum clean all && rm -rf /var/cache/yum

# Add container startup and management scripts.
COPY dockerfile_exec.sh .
COPY iam.py .
COPY login_page.html .

# Create a non-root user and group for the application to run as to guard against
# run-time modification of the system and application.
RUN groupadd application && \
    useradd -g application -d /home/application -s /sbin/nologin -c "application process" application && \
    chown -R application:application /home/application
RUN echo -n "the non-root user is: " && grep ^application /etc/passwd

# Give the non-root user access to scratch space.
RUN mkdir -p local
RUN chown -R application:application local

# Run the container's process zero as this user.
USER application

# HOST parameter
# ARG HOST

# Set the startup script.
CMD [ "bash", "dockerfile_exec.sh" ]
