#include<iostream>
#include<string>
#include<fstream>
#include<winsock2.h>
#include<ws2tcpip.h>
#include<filesystem>

// recieves the ip address of the reciever
std::string get_sending_information(int port){

	SOCKET udp_socket = socket(AF_INET, SOCK_DGRAM, 0);

	BOOL broadcast = TRUE;
	setsockopt(udp_socket, SOL_SOCKET, SO_BROADCAST, (char*)&broadcast, sizeof(broadcast));

	sockaddr_in broadcastAddr{};
	broadcastAddr.sin_family = AF_INET;
	broadcastAddr.sin_port = htons(port);
	broadcastAddr.sin_addr.s_addr = INADDR_ANY;

	bind(udp_socket,(sockaddr*)&broadcastAddr, sizeof(broadcastAddr));

	timeval to;
	to.tv_sec = 5;
	to.tv_usec = 0;
	setsockopt(udp_socket, SOL_SOCKET, SO_RCVTIMEO, (char*) &to, sizeof(to));

	char buffer[1024];

	sockaddr_in sender;
	socklen_t sender_len = sizeof(sender);
	recvfrom(udp_socket, buffer, sizeof(buffer), 0, (sockaddr *)&sender, &sender_len);

	closesocket(udp_socket);
	return buffer;

}

void interpret_message(std::string message, std::string ip_address, std::string port){

	size_t ip_start_pos = message.find("IP:");
	size_t ip_end_pos = message.find("PORT:");

	ip_address = message.substr(ip_start_pos+3, ip_end_pos);
	port = message.substr(ip_end_pos+5);

}

void file_sender(std::string ip_address, std::string filename, int port){

	SOCKET tcp_socket = socket(AF_INET, SOCK_STREAM, 0);

	struct sockaddr_in sender;
	sender.sin_family = AF_INET;
	sender.sin_port = htons(port);
	inet_pton(AF_INET, ip_address.c_str(), &sender.sin_addr);

	connect(tcp_socket, (struct sockaddr *)&sender, sizeof(sender));


	std::ifstream file(filename.c_str(), std::ios::binary);
	uint64_t file_size = std::filesystem::file_size(filename.c_str());
	int total_bytes_sent = 0;
	ssize_t send_request_bytes;
	while ( total_bytes_sent < sizeof(file_size) ) {

		send_request_bytes = send(tcp_socket, reinterpret_cast<char*>(&file_size), sizeof(file_size), 0);
		if ( send_request_bytes <= 0 ){
			std::cout << "Tcp failed.";
		} else {
			total_bytes_sent += send_request_bytes;
		}
	}


	char buffer[1024*64]; // 64kb
	total_bytes_sent = 0;
	send_request_bytes = 0;
	while ( file ){ // is file valid to read

		while( file.read(buffer, sizeof(buffer)) || file.gcount() ) {

			send_request_bytes = send(tcp_socket, buffer, sizeof(buffer), 0);

			if (send_request_bytes <= 0){
				std::cout << "Sending files failed.";
			} else {
				total_bytes_sent += send_request_bytes;
			}
		}
	}

	file.close();
	closesocket(tcp_socket);
}

int main(){

	WSADATA wsa;
	WSAStartup(MAKEWORD(2, 2), &wsa);

	int input_port = 5000;
	std::string ip_addr;
	std::string output_port;
	std::string filename = "";

	std::string message = get_sending_information(input_port);
	interpret_message(message, ip_addr, output_port);
	file_sender(ip_addr, filename, stoi(output_port));

	WSACleanup();

	return 0;

}

