#include<iostream>
#include<string>
#include<fstream>
#include<winsock2.h>
#include<ws2tcip.h>
#include<libssh2.h>
#include<libssh2_sftp.h>


int main(){

	std::string filepath = "C:\\Users\\Administrator\\Downloads\\w7_calc.exe";
	std::string hostname = "";
	int port = 22;

	WSADATA wsa;
	WSAStartup(MAKEWORD(2, 2), &wsa);


	addrinfo hints{}, *info;

	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;

	INT get_addrinfo_result = getaddrinfo(hostname, &hints, &info);
	if (get_addrinfo_result != 0){
		std::cerr << "getaddrinfo failed.";
		return 0;
	}

	SOCKET sock_ = socket(info->ai_family, info->ai_socktype, info->ai_protocol);

	int connect_result = connect(sock, info->ai_addr, (int)info->ai_addrlen);
	if (connect_result != 0){
		std::cerr << "connect failed.";
		return 0;
	}

	WSACleanup();


}
