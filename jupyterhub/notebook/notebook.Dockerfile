FROM quay.io/jupyter/datascience-notebook:2024-12-23

ENV TINI_VERSION=v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

WORKDIR /home/jovyan

ENTRYPOINT ["/tini", "--"]

CMD ["start-notebook.py"]
