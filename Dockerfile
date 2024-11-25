ARG UBUNTU_VERSION=20.04
FROM ubuntu:${UBUNTU_VERSION}

ARG ERLANG_VERSION
ARG ELIXIR_VERSION
ARG ERLANG_DOWNLOAD_URL
ARG ERLANG_DOWNLOAD_SHA256
ARG ELIXIR_DOWNLOAD_URL
ARG ELIXIR_DOWNLOAD_SHA256

ENV LANG=C.UTF-8

# Install Erlang
RUN set -xe \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        autoconf \
        libncurses5-dev \
        libssl-dev \
        curl \
        git \
        ca-certificates \
        wget \
    && curl -fSL -o otp-src.tar.gz "${ERLANG_DOWNLOAD_URL}" \
    && echo "${ERLANG_DOWNLOAD_SHA256}  otp-src.tar.gz" | sha256sum -c - \
    && mkdir -p /usr/src/otp \
    && tar -xzf otp-src.tar.gz -C /usr/src/otp --strip-components=1 \
    && rm otp-src.tar.gz \
    && cd /usr/src/otp \
    && ./otp_build autoconf \
    && ./configure \
    && make -j$(nproc) \
    && make install \
    && cd .. \
    && rm -rf /usr/src/otp

# Install Elixir
RUN set -xe \
    && curl -fSL -o elixir-src.tar.gz "${ELIXIR_DOWNLOAD_URL}" \
    && echo "${ELIXIR_DOWNLOAD_SHA256}  elixir-src.tar.gz" | sha256sum -c - \
    && mkdir -p /usr/local/src/elixir \
    && tar -xzf elixir-src.tar.gz -C /usr/local/src/elixir --strip-components=1 \
    && rm elixir-src.tar.gz \
    && cd /usr/local/src/elixir \
    && make install clean \
    && find /usr/local/src/elixir/ -type f -not -regex "/usr/local/src/elixir/lib/[^\/]*/lib.*" -exec rm -rf {} + \
    && find /usr/local/src/elixir/ -type d -depth -empty -delete \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["iex"]
