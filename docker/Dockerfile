FROM alpine:3.21.3

# ENV LIGHTTPD_VERSION=1.4.76-r0
ENV DCATAPEIA_VERSION=../drafts/0.0.1-draft-0.1

RUN addgroup -S --gid 1000 lighttpd \
    && adduser -S -G lighttpd --uid 1000 lighttpd

# RUN apk add --update --no-cache lighttpd=${LIGHTTPD_VERSION} \
RUN apk add --update --no-cache lighttpd \
    && rm -rf /var/cache/apk/* \
    && chgrp lighttpd /usr/sbin/lighttpd

COPY --chown=:lighttpd ./docker/lighttpd.conf /etc/lighttpd/lighttpd.conf

WORKDIR /var/www/html
COPY --chown=:lighttpd ./releases/${DCATAPEIA_VERSION}/codelists ./resource
COPY --chown=:lighttpd ./releases/${DCATAPEIA_VERSION}/doc-eia.html ./doc-eia-latest.html
COPY --chown=:lighttpd ./releases/${DCATAPEIA_VERSION}/DCAT-AP.EIA.jpg .
COPY --chown=:lighttpd ./releases/${DCATAPEIA_VERSION}/styles ./styles
COPY --chown=:lighttpd ./releases ./releases
COPY --chown=:lighttpd ./docker/static .
RUN find . -name "index.html" -exec sed -i "s@{DCATAPEIA_VERSION}@${DCATAPEIA_VERSION}@g" {} + && \
    for version in $(ls -d ./releases/* | xargs -n 1 basename); do \
        list_items="${list_items}<li><a href=\"./${version}/\" title=\"Dokumentation zu DCAT-AP.EIA Release ${version}\">${version}</a></li>"; \
    done && echo "list_items: ${list_items}" && \
    sed -i "s@{RELEASES}@${list_items}@" ./index.html

EXPOSE 8080 443

USER lighttpd

ENTRYPOINT ["/usr/sbin/lighttpd"]
CMD ["-D", "-f", "/etc/lighttpd/lighttpd.conf"]