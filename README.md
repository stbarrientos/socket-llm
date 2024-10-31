## Local LLM

This project is  simple POC to have a locally installed LLM that listens and responds to prompts over a socket server.

Eventually, I'd like to use this server as a service for more complicated web apps to use an LLM that exists side by side on the same machine, without needing to connect to a third party API.

## Rust Socket Client

This project also includes a Rust socket client that sends a message to port 65432 and listens for a response.

### Building the Rust Socket Client

1. Ensure you have Rust installed. If not, you can install it from [rust-lang.org](https://www.rust-lang.org/).
2. Navigate to the `rust` directory.
3. Run `cargo build` to build the project.

### Running the Rust Socket Client

1. After building the project, run `cargo run` to start the Rust socket client.
2. The client will send a message to port 65432 and print the response from the server.
