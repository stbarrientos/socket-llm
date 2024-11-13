FROM python:3.9 AS python-base

WORKDIR /usr/llm/app

COPY ./requirements.txt /usr/llm/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /usr/llm/requirements.txt

EXPOSE 65432

FROM python-base AS server

CMD [ "python", "server.py" ]

FROM python-base AS test

CMD [ "python", "-m", "unittest", "discover", "-s", "./test" ]

# Build stage for Rust client
FROM rust:latest AS rust-client

COPY ./rust /usr/llm/rust-client
WORKDIR /usr/llm/rust-client

# Build the Rust client
RUN cargo build --release

CMD [ "cargo", "run" ]
