# syntax=docker/dockerfile:1
#
# phys2bids container image.
#
# Build:  docker build -t phys2bids .
# Run:    docker run --rm -v "$PWD":/data -w /data phys2bids -h

ARG PYTHON_VERSION=3.12

# ---- Build stage: install phys2bids and its optional readers into a venv ----
FROM python:${PYTHON_VERSION}-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /src
COPY . .

# versioneer reads the version from git metadata, so .git must be present in
# the build context (it is not copied into the final image).
RUN pip install --upgrade pip \
    && pip install ".[acq,mat]"

# ---- Runtime stage: only the virtualenv, no build tooling or sources ----
FROM python:${PYTHON_VERSION}-slim

LABEL org.opencontainers.image.title="phys2bids" \
      org.opencontainers.image.description="Python library to convert physiological data files into BIDS format" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.source="https://github.com/physiopy/phys2bids"

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Run as an unprivileged user; mount data at /data.
RUN useradd --create-home --uid 1000 phys2bids \
    && mkdir /data \
    && chown phys2bids:phys2bids /data
USER phys2bids
WORKDIR /data

ENTRYPOINT ["phys2bids"]
CMD ["-h"]
