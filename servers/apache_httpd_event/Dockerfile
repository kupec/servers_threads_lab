FROM httpd

COPY index.lua ./htdocs
COPY httpd.conf ./conf
COPY config_base .
COPY config_override .
RUN { cat config_base; cat config_override; } >> conf/httpd.conf
