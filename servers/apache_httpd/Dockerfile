FROM httpd

ARG variant

COPY index.lua ./htdocs
COPY httpd.conf ./conf
COPY config_base .
COPY config_$variant .
RUN { cat config_base; cat config_$variant; } >> conf/httpd.conf
