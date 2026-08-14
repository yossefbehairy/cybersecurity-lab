FROM debian:12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      dnsutils \
      iproute2 \
      jq \
      netcat-openbsd \
      nmap \
      postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/sh analyst

USER analyst
WORKDIR /home/analyst

CMD ["sh"]

