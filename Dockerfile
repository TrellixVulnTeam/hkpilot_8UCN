FROM centos:8

RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*


RUN yum update -y && yum install -y epel-release && \
    yum install -y dnf-plugins-core &&\
    yum config-manager -y --set-enabled powertools && \
    yum install git make cmake3 gcc-c++ gcc binutils libX11-devel libXpm-devel libXft-devel libXext-devel python38 openssl-devel &&\
    yum install -y redhat-lsb-core gcc-gfortran pcre-devel \
        mesa-libGL-devel mesa-libGLU-devel glew-devel ftgl-devel mysql-devel \
        fftw-devel cfitsio-devel graphviz-devel libuuid-devel \
        avahi-compat-libdns_sd-devel openldap-devel python38 \
        python38-pip \
        python38-devel \
        python38-numpy \
        libxml2-devel gsl-devel readline-devel qt5-qtwebengine-devel \
        R-devel R-Rcpp-devel R-RInside-devel \
        git openssh-clients

RUN ln -sfn /usr/bin/python3.8 /usr/bin/python3 & \
    ln -sfn /usr/bin/python3 /usr/bin/python & \
    ln -sfn /usr/bin/pip3.8 /usr/bin/pip3 & \
    ln -sfn /usr/bin/pip3 /usr/bin/pip

RUN yum clean -y all

RUN mkdir /usr/local/hk
WORKDIR /usr/local/hk