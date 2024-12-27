use std::io::{Read, Write};
use std::net::TcpStream;

fn main() {
    // Connect to the server at port 65432
    match TcpStream::connect("127.0.0.1:65432") {
        Ok(mut stream) => {
            println!("Successfully connected to server at port 65432");

            // Send a message to the server
            let msg = b"What is the capital of the USA?";
            stream.write(msg).unwrap();
            stream.write(b"__close__").unwrap();
            println!("Sent message: {}", String::from_utf8_lossy(msg));

            // Read the response from the server
            let mut temp_buffer = [0; 512];
            loop {
                match stream.read(&mut temp_buffer) {
                    Ok(n) => {
                        if n == 0 {
                            break;
                        }
                        let message = String::from_utf8_lossy(&temp_buffer[..n]);
                        println!("Received message: {}", message);
                        if message.ends_with("__close__") {
                            println!("Closing connection");
                            break;
                        }
                    }
                    Err(e) => {
                        println!("Failed to receive data: {}", e);
                        break;
                    }
                }
            }
        }
        Err(e) => {
            println!("Failed to connect: {}", e);
        }
    }
}
