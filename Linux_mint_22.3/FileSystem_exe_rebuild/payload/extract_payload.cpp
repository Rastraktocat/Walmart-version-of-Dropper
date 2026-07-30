#include<iostream>
#include<string>
#include<fstream>
#include<winsock2.h>
#include<ws2tcpip.h>
#include<libssh2.h>
#include<libssh2_sftp.h>
#include<filesystem>

// recieves the ip address of the reciever
std::string get_sending_information(){

	SOCKET udp_socket = socket(AF_INET, SOCK_DGRAM, 0);

	BOOL broadcast = TRUE;
	setsockopt(udp_socket, SOL_SOCKET, SO_BROADCAST, (char*)&broadcast, sizeof(broadcast));

	sockaddr_in broadcastAddr{};
	broadcastAddr.sin_family = AF_INET;
	broadcastAddr.sin_port = htons();
	broadcastAddr.sin_addr.s_addr = INADDR_ANY;

	bind(udp_socket,(sockaddr*)&broadcastAddr, sizeof(broadcastAddr));

	timeval to;
	to.tv_sec = 5;
	to.tv_usec = 0;
	setsockopt(udp_socket, SOL_SOCKET, SO_RCVTIMEO, &to, sizeof(to));

	char buffer[1024];

	sockaddr_in sender;
	socklen_t sender_len = sizeof(sender);
	recvfrom(upd_socket, buffer, sizeof(buffer), 0, (sockaddr *)&sender, &sender_len);

	closesocket(udp_socket);
	return buffer;

}

void file_sender(char* ip_address, char* filename, int port){

	SOCKET tcp_socket = socket(AF_INET, SOCK_STREAM, 0);

	struct sockadder_in sender;
	sender.sin_family = AF_INET;
	sender.sin_port = htons(port);
	inet_pton(AF_INET, ip_address, &sender.sin_addr);

	connect(tcp_socket, (struct sockaddr *)&sender, sizeof(sender));


	std::ifstream file(filename, std::ios::binary);
	uint64_t file_size = std::filesystem::filesize(filename);
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
	close(tcp_socket);
}

int main(){

	WSADATA wsa;
	WSAStartup(MAKEWORD(2, 2), &wsa);

	char* message = get_sending_information();
	file_sender();

	WSACleanup();

	return 0;

}

