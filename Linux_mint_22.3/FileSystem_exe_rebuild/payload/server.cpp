#include<stdio.h>
#include<winsock2.h>
#include<windows.h>
#include<ws2tcpip.h>
#include<winhttp.h>
#include<fstream>

std::string get_public_ip(){

	std::string ip_address;

	HINTERNET h_session = WinHttpOpen(L"IP Lookup Client/1.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
	if (!h_session){
		return "Failed to get IP address.";
	}

	HINTERNET h_connect = WinHttpConnect(h_session, L"api.ipify.org", INTERNET_DEFAULT_HTTPS_PORT, 0);
	if (!h_connect) {
		WinHttpCloseHandle(h_session);
		return "Failed to get IP address.";
	}

	HINTERNET h_request = WinHttpOpenRequest(h_connect, L"GET", L"/", nullptr, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, WINHTTP_FLAG_SECURE);
	if (!h_request) {
		WinHttpCloseHandle(h_session);
		WinHttpCloseHandle(h_connect);
		return "Failed to get IP address.";
	}

	BOOL result = WinHttpSendRequest(h_request, WINHTTP_NO_ADDITIONAL_HEADERS, 0, WINHTTP_NO_REQUEST_DATA, 0, 0, 0);
	if ( result ) {
		result = WinHttpReceiveResponse(h_request, nullptr);

		DWORD available_bytes = 0;
		while (WinHttpQueryDataAvailable(h_request, &available_bytes) && available_bytes > 0) {
			std::string buffer(available_bytes, '\0');
			DWORD read_bytes = 0;

			if (WinHttpReadData(h_request, buffer.data(), available_bytes, &read_bytes)) {
				ip_address.append(buffer.data(), read_bytes);
			} else {
				break;
			}
		}

	}

	WinHttpCloseHandle(h_request);
	WinHttpCloseHandle(h_connect);
	WinHttpCloseHandle(h_session);
	return ip_address;

}

void send_information(char* ip_address, char* message, int port){

	int udp_socket = socket(AF_INET, SOCK_DGRAM, 0);

	int broadcast = 1;

	setsockopt(udp_socket, SOL_SOCKET, SO_BROADCAST, (char*) &broadcast, sizeof(broadcast));

	sockaddr_in addr = {};
	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);
	addr.sin_addr.s_addr = INADDR_BROADCAST;

	sendto(udp_socket, message, strlen(message), 0, (sockaddr*)&addr, sizeof(addr));

	closesocket(udp_socket);

}

void get_file_information(char* ip_address, char* filename, int port){

	int server = socket(AF_INET, SOCK_STREAM, 0);

	sockaddr_in server_addr = {};
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(port);
	inet_pton(AF_INET, ip_address, &server_addr.sin_addr);

	char ip[INET_ADDRSTRLEN];
	sockaddr_in client_addr = {};
	int client_size = sizeof(client_addr);
	inet_ntop(AF_INET, &client_addr.sin_addr, ip, sizeof(ip));

	bind(server, (sockaddr*)&server_addr, sizeof(server_addr));
	listen(server, SOMAXCONN);
	SOCKET client = accept(server, (sockaddr*)&client_addr, &client_size);

	char buffer[1024 * 64]; // 64kb
	std::ofstream file(filename, std::ios::binary);

	while( file ){

		int incoming_length = recv(client, buffer, sizeof(buffer), 0);

		if (incoming_length <= 0){
			break;
		}

		file.write(buffer, incoming_length);

	}

	file.close();
	closesocket(client);
	closesocket(server);

}

int main(){

	WSADATA wsa;
	WSAStartup(MAKEWORD(2,2), &wsa);

	char* server_ip_address = get_public_ip();
	char* connected_ip_address = "";
	int udp_port = 5000;
	int tcp_port = 5001;

	std::string message = "IP:";
	message += server_ip_address;
	message += "PORT=";
	message += std::to_string(tcp_port);

	send_information(connected_ip_address, message.c_str(), udp_port);
	get_file_information(connected_ip_address, "w7_calc.exe", tcp_port);

	WSACleanup();

	return 0;
}
