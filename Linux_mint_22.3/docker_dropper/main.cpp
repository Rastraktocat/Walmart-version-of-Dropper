#include<string.h>
#include<fstream>
#include<arpa/inet.h>
#include<unistd.h>
#include<iostream>
#include<sys/socket.h>
#include<netinet/in.h>

int server_fd;
int client_fd;
sockaddr_in server_addr{};
sockaddr_in client_addr{};
socklen_t client_len;
const char[4096] recieved_message;

int port = 8080;
std::string filename = "out/log.txt";

int setup_connection();
int recieve_message();
int log_message(std::string, std::string);

int setup_connection(){

	server_fd = socket(AF_INET, SOCK_STREAM, 0);
	if (server_fd < 0){
		perror("socket");
		return 1;
	}

	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.s_addr = INADDR_ANY;
	server_addr.sin_port = htons(port);

	if (bind(server_fd, reinterpret_cast<sockaddr*>(&server_addr), sizeof(server_addr)) < 0){
		perror("bind");
		close(server_fd);
		return 1;
	}

	if (listen(server_fd, 10) < 0) {
		perror("listen");
		close(server_fd);
		return 1;
	}

	return 0;

}

int recieve_message(){

	client_len = sizeof(client_addr);
	client_fd = accept(server_fd, reinterpret_cast<sockaddr*>(&clientaddr), &client_len);
	if (client_fd < 0){
		perror("accept");
		close(server_fd);
		return 1;
	}

	void* rec_message = reinterpret_cast<void*>(&recieved_message);
	ssize_t bytes = recv(client_fd, rec_message, sizeof(recieved_message), 0);
	if (bytes < 0){
		perror("recv");
		close(server_fd);
		close(client_fd);
		return 1;
	}

	buffer[bytes] = '\0';
	recieved_message = buffer;

	close(server_fd);
	close(client_fd);
	return 0;

}

int log_message(std::string log_file, std::string message){

	std::ofstream file(log_file, std::ios::app);

	if (!file.is_open()){
		std::cerr << "File Logging error";
		close(server_fd);
		close(client_fd);
		return 1;
	}

	file << message;
	return 0;

}


int main(){

	int setup = setup_connection();
	if (setup == 1){
		return 1;
	}

	int recieve = recieve_message();
	if (recieve == 1){
		return 1;
	}

	int log = log_message(filename, recieved_message);
	if (log == 1){
		return 1;
	}

	return 0;

}
