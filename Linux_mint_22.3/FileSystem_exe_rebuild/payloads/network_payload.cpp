#include <iostream>
#include <cstring>
#include <winsock2.h>
#include <ws2tcpip.h>

std::string message = "This is a message sent from the dropper";

int result;

int send_message(std::string client_message) {

	WSADATA wsaData;
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
		std::cerr << "WSAStartup failed.\n";
		return 1;
	}

	SOCKET client_connect = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (client_connect == INVALID_SOCKET){
		std::cerr << "Socket failed.\n";
		return 1;
	}

	sockaddr_in client_addr{};
	client_addr.sin_family = AF_INET;
	client_addr.sin_port = htons(8080);
	client_addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

	if (connect(client_connect, reinterpret_cast<sockaddr*>(&client_addr), sizeof(client_addr)) == SOCKET_ERROR){
		std::cerr << "Connect failed.\n";
		closesocket(client_connect);
		WSACleanup();
		return 1;
	}

	int bytes = send(client_connect, client_message.c_str(), client_message.size(), 0);
	if (bytes == SOCKET_ERROR){
		std::cerr << "Send failed.\n";
		closesocket(client_connect);
		return 1;
	} else {
		std::cout << "Sent: " << bytes << " bytes";
	}

	closesocket(client_connect);
	WSACleanup();
	return 0;

}

int main() {

	int result = send_message(message);
	return result;
}
