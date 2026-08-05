#include<windows.h>
#include<winhttp.h>
#include<fstream>
#include<stdio.h>
#include<cstdlib>
#include<iostream>

void CALLBACK StatusCallback(
    HINTERNET hInternet,
    DWORD_PTR context,
    DWORD status,
    LPVOID info,
    DWORD infoLen)
{
    std::cout << "Status: 0x" << std::hex << status << std::dec << '\n';

    switch (status)
    {
    case WINHTTP_CALLBACK_STATUS_RESOLVING_NAME:
        std::cout << "Resolving name\n";
        break;

    case WINHTTP_CALLBACK_STATUS_NAME_RESOLVED:
        std::cout << "Name resolved\n";
        break;

    case WINHTTP_CALLBACK_STATUS_CONNECTING_TO_SERVER:
        std::cout << "Connecting\n";
        break;

    case WINHTTP_CALLBACK_STATUS_CONNECTED_TO_SERVER:
        std::cout << "Connected\n";
        break;

    case WINHTTP_CALLBACK_STATUS_SENDING_REQUEST:
        std::cout << "Sending request\n";
        break;

    case WINHTTP_CALLBACK_STATUS_REQUEST_SENT:
        std::cout << "Request sent\n";
        if (info && infoLen == sizeof(DWORD))
            std::cout << "Bytes sent: " << *(DWORD*)info << '\n';
        break;

    case WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE:
        std::cout << "SendRequest complete\n";
        break;

    case WINHTTP_CALLBACK_STATUS_RECEIVING_RESPONSE:
        std::cout << "Receiving response\n";
        break;

    case WINHTTP_CALLBACK_STATUS_RESPONSE_RECEIVED:
        std::cout << "Response received\n";
        break;

    case WINHTTP_CALLBACK_STATUS_HEADERS_AVAILABLE:
        std::cout << "Headers available\n";
        break;

    case WINHTTP_CALLBACK_STATUS_DATA_AVAILABLE:
        std::cout << "Data available\n";
        break;

    case WINHTTP_CALLBACK_STATUS_READ_COMPLETE:
        std::cout << "Read complete\n";
        break;

    case WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING:
        std::cout << "Handle closing\n";
        break;

    case WINHTTP_CALLBACK_STATUS_CONNECTION_CLOSED:
        std::cout << "Connection closed\n";
        break;

    case WINHTTP_CALLBACK_STATUS_REQUEST_ERROR:
    {
        auto* err = static_cast<WINHTTP_ASYNC_RESULT*>(info);
        if (err)
        {
            std::cout << "Request error\n";
            std::cout << "API: " << err->dwResult << '\n';
            std::cout << "Error: " << err->dwError << '\n';
        }
        break;
    }

    case WINHTTP_CALLBACK_STATUS_SECURE_FAILURE:
    {
        DWORD flags = *(DWORD*)info;
        std::cout << "Secure failure flags: 0x"
                  << std::hex << flags << std::dec << '\n';
        break;
    }

    default:
        std::cout << "Unknown status: 0x"
                  << std::hex << status << std::dec << '\n';
        break;
    }
}

std::string get_public_ip(){

    std::string ip_address;

    HINTERNET h_session = WinHttpOpen(
        L"IP Lookup Client/1.0",
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0);

    if (!h_session)
        return "WinHttpOpen failed: " + std::to_string(GetLastError());

    WINHTTP_STATUS_CALLBACK prev = WinHttpSetStatusCallback(
	h_session,
	StatusCallback,
	WINHTTP_CALLBACK_FLAG_SECURE_FAILURE |
	WINHTTP_CALLBACK_FLAG_SENDREQUEST_COMPLETE |
	WINHTTP_CALLBACK_FLAG_REQUEST_ERROR |
	WINHTTP_CALLBACK_FLAG_SEND_REQUEST |
	WINHTTP_CALLBACK_FLAG_HEADERS_AVAILABLE,
	0
    );

    if ( prev == WINHTTP_INVALID_STATUS_CALLBACK ) {
	DWORD err = GetLastError();
	return "WinHttpSetStatusCallback failed: " + std::to_string(err);

    }
#ifdef WINHTTP_FLAG_SECURE_PROTOCOL_TLS1_2

    DWORD protocols = WINHTTP_FLAG_SECURE_PROTOCOL_TLS1_2;

    if (!WinHttpSetOption(h_session, WINHTTP_OPTION_SECURE_PROTOCOLS, &protocols, sizeof(protocols))) {
	return "WinHttpSetOption(TLS 1.2) failed: " + std::to_string(GetLastError());
    }

#endif

    HINTERNET h_connect = WinHttpConnect( h_session, L"microsoft.com", INTERNET_DEFAULT_HTTPS_PORT, 0);

    if (!h_connect) {
        DWORD err = GetLastError();
        WinHttpCloseHandle(h_session);
        return "WinHttpConnect failed: " + std::to_string(err);
    }


    HINTERNET h_request = WinHttpOpenRequest(
        h_connect,
        L"GET",
        L"/",
        nullptr,
        WINHTTP_NO_REFERER,
        WINHTTP_DEFAULT_ACCEPT_TYPES,
       	WINHTTP_FLAG_SECURE);

    if (!h_request)
    {
        DWORD err = GetLastError();
        WinHttpCloseHandle(h_connect);
        WinHttpCloseHandle(h_session);
        return "WinHttpOpenRequest failed: " + std::to_string(err);
    }

//    if (!WinHttpAddRequestHeaders(h_request, L"User-Agent: Mozilla/5.0\r\nAccept: text/plain\r\n", -1, WINHTTP_ADDREQ_FLAG_ADD)) {
//
//	WinHttpCloseHandle(h_request);
//	WinHttpCloseHandle(h_connect);
//	WinHttpCloseHandle(h_session);
//	return "WinHttpAddRequestHeaders failed: " + std::to_string(GetLastError());

  // }

    // Send request
    if (!WinHttpSendRequest(
            h_request,
            WINHTTP_NO_ADDITIONAL_HEADERS,
            0,
            WINHTTP_NO_REQUEST_DATA,
            0,
            0,
            0))
    {
        DWORD err = GetLastError();
        WinHttpCloseHandle(h_request);
        WinHttpCloseHandle(h_connect);
        WinHttpCloseHandle(h_session);
        return "WinHttpSendRequest failed: " + std::to_string(err);
    }

    // Receive response
    if (!WinHttpReceiveResponse(h_request, nullptr))
    {
        DWORD err = GetLastError();
        WinHttpCloseHandle(h_request);
        WinHttpCloseHandle(h_connect);
        WinHttpCloseHandle(h_session);
        return "WinHttpReceiveResponse failed: " + std::to_string(err);
    }

    // Check HTTP status
    DWORD status = 0;
    DWORD size = sizeof(status);

    if (!WinHttpQueryHeaders(
            h_request,
            WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
            WINHTTP_HEADER_NAME_BY_INDEX,
            &status,
            &size,
            WINHTTP_NO_HEADER_INDEX))
    {
        DWORD err = GetLastError();
        WinHttpCloseHandle(h_request);
        WinHttpCloseHandle(h_connect);
        WinHttpCloseHandle(h_session);
        return "WinHttpQueryHeaders failed: " + std::to_string(err);
    }

    if (status != 200)
    {
        WinHttpCloseHandle(h_request);
        WinHttpCloseHandle(h_connect);
        WinHttpCloseHandle(h_session);
        return "HTTP status code: " + std::to_string(status);
    }

    // Read body
    DWORD available_bytes = 0;

    while (true)
    {
        if (!WinHttpQueryDataAvailable(h_request, &available_bytes))
        {
            DWORD err = GetLastError();
            WinHttpCloseHandle(h_request);
            WinHttpCloseHandle(h_connect);
            WinHttpCloseHandle(h_session);
            return "WinHttpQueryDataAvailable failed: " + std::to_string(err);
        }

        if (available_bytes == 0)
            break;

        std::string buffer(available_bytes, '\0');
        DWORD read_bytes = 0;

        if (!WinHttpReadData(
                h_request,
                buffer.data(),
                available_bytes,
                &read_bytes))
        {
            DWORD err = GetLastError();
            WinHttpCloseHandle(h_request);
            WinHttpCloseHandle(h_connect);
            WinHttpCloseHandle(h_session);
            return "WinHttpReadData failed: " + std::to_string(err);
        }

        ip_address.append(buffer.data(), read_bytes);
    }

    WinHttpCloseHandle(h_request);
    WinHttpCloseHandle(h_connect);
    WinHttpCloseHandle(h_session);

    if (ip_address.empty())
        return "Received an empty response.";

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
    file.close();

}

void pop_out_file(){

    STARTUPINFOW si{};
    PROCESS_INFORMATION pi{};
    si.cb = sizeof(si);

    std::wstring cmd = L"C:\\Windows\\System32\\notepad.exe C:\\Users\\Administrator\\Downloads\\file_output.txt";

    DWORD attr = GetFileAttributesW(L"C:\\Users\\Administrator\\Downloads\\file_output.txt");
    if (attr == INVALID_FILE_ATTRIBUTES) {
	    MessageBoxW(nullptr, L"File does not exist!", L"Debug", MB_OK);
    }

    int result = CreateProcessW(nullptr, &cmd[0], nullptr, nullptr, FALSE, 0, nullptr, nullptr, &si, &pi);
    if (result == 0) {
        std::cout << "CreateProcess failed: " << std::to_string(GetLastError());
    }
}

int main(){

    LoadLibraryW(L"mscoree.dll");

    file_setup();
    std::cout << "\nfile_setup ran \n";
    pop_out_file();

}
