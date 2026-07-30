#include<windows.h>
#include<winhttp.h>
#include<fstream>
#include<stdio.h>
#include<cstdlib>
#include<iostream>

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
		WinHttpCloseHandle(h_connect);
		WinHttpCloseHandle(h_session);
		return "Failed to get IP address.";
	}

	BOOL result = WinHttpSendRequest(h_request, WINHTTP_NO_ADDITIONAL_HEADERS, 0, WINHTTP_NO_REQUEST_DATA, 0, 0, 0);
	if ( result ) {
		result = WinHttpReceiveResponse(h_request, nullptr);
		if ( !result ) {
			WinHttpCloseHandle(h_request);
			WinHttpCloseHandle(h_connect);
			WinHttpCloseHandle(h_session);
			return "Failed to Get IP address";
		}

		DWORD status = 0;
		DWORD size = sizeof(status);
		WinHttpQueryHeaders(h_request, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER, WINHTTP_HEADER_NAME_BY_INDEX, &status, &size, WINHTTP_NO_HEADER_INDEX);
		if (status != 200){
			ip_address = "Failed to Get IP address: ";
			ip_address += std::to_string(status);
			return ip_address;

		}

		DWORD available_bytes = 0;
		while (!WinHttpQueryDataAvailable(h_request, &available_bytes) && available_bytes > 0) {
			std::string buffer(available_bytes, '\0');
			DWORD read_bytes = 0;

			if (WinHttpReadData(h_request, buffer.data(), available_bytes, &read_bytes)) {
				ip_address.append(buffer.data(), read_bytes);
			} else {
				break;
			}
		}

	} else {
		WinHttpCloseHandle(h_session);
		WinHttpCloseHandle(h_connect);
	}

	WinHttpCloseHandle(h_request);
	WinHttpCloseHandle(h_connect);
	WinHttpCloseHandle(h_session);
	std::cout << "This is the ip address: " << ip_address;
	return ip_address;

}

void file_setup(){

    std::string ip_address = get_public_ip();
    std::string final_ip_addr = "[ " + ip_address + " ]";
    std::string filepath = "C:\\Users\\Administrator\\Downloads\\file_output.txt";

    std::ofstream file(filepath);
    if (!file.is_open()){
	std::cout << "file failed to create.";
	return ;
    }

    file.write(final_ip_addr.c_str(), final_ip_addr.size());
    if (!file.good()){
	std::cout << "File failed to write.";
        return ;
    }

}

void pop_out_file(){

    STARTUPINFOW si{};
    PROCESS_INFORMATION pi{};
    si.cb = sizeof(si);

    std::wstring cmd = L"C:\\Windows\\System32\\notepad.exe C:\\Users\\Administrator\\Downloads\\file_output.txt";

    int result = CreateProcessW(nullptr, &cmd[0], nullptr, nullptr, FALSE, 0, nullptr, nullptr, &si, &pi);
    if (result == 0) {
        std::cout << "CreateProcess failed: " << GetLastError();
    }
}

int main(){

    LoadLibraryW(L"mscoree.dll");

    file_setup();
    pop_out_file();

}
