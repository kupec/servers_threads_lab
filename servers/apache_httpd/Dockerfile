FROM httpd:alpine
COPY index.lua ./htdocs
COPY config .
RUN cat config >> conf/httpd.conf
