FROM quay.io/jupyter/datascience-notebook:2024-12-23

USER root
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

ENV TINI_VERSION=v0.19.0
RUN curl -L https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini -o /tini \
    && chown root:root /tini \
    && chmod +x /tini

WORKDIR /srv/jupyterhub

ENTRYPOINT ["/tini", "--"]

CMD ["start-notebook.py"]
