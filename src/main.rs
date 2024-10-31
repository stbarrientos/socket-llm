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
            println!("Sent message: {}", String::from_utf8_lossy(msg));

            // Read the response from the server
            let mut buffer = [0; 1024];
            match stream.read(&mut buffer) {
                Ok(_) => {
                    let response = String::from_utf8_lossy(&buffer);
                    println!("Received response: {}", response);
                }
                Err(e) => {
                    println!("Failed to receive data: {}", e);
                }
            }
        }
        Err(e) => {
            println!("Failed to connect: {}", e);
        }
    }
}
