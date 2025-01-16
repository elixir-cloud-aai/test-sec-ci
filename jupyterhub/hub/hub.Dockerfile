FROM quay.io/jupyterhub/jupyterhub:5.2.1

ENV TINI_VERSION=v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

WORKDIR /srv/jupyterhub

ENTRYPOINT ["/tini", "--"]

CMD ["jupyterhub"]
