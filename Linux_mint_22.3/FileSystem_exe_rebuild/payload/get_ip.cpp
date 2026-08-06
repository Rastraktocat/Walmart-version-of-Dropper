#include<windows.h>
#include<winhttp.h>
#include<fstream>
#include<stdio.h>
#include<cstdlib>
#include<iostream>

std::string g_statusCallback = "";

void CALLBACK StatusCallback(
    HINTERNET,
    DWORD_PTR,
    DWORD status,
    LPVOID info,
    DWORD infoLen)
{
    switch (status)
    {
        break;
    case WINHTTP_CALLBACK_STATUS_NAME_RESOLVED:
        g_statusCallback += "Name resolved\n";
        break;

    case WINHTTP_CALLBACK_STATUS_CONNECTING_TO_SERVER:
        g_statusCallback += "Connecting to server\n";
        break;

    case WINHTTP_CALLBACK_STATUS_CONNECTED_TO_SERVER:
        g_statusCallback += "Connected to server\n";
        break;

    case WINHTTP_CALLBACK_STATUS_SENDING_REQUEST:
        g_statusCallback += "Sending request\n";
        break;

    case WINHTTP_CALLBACK_STATUS_REQUEST_SENT:
    {
        g_statusCallback += "Request sent";

        if (info && infoLen == sizeof(DWORD))
            g_statusCallback +=
                " (" + std::to_string(*(DWORD*)info) + " bytes)\n";
        break;
    }

    case WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE:
        g_statusCallback += "SendRequest complete\n";
        break;

    case WINHTTP_CALLBACK_STATUS_RECEIVING_RESPONSE:
        g_statusCallback += "Receiving response\n";
        break;

    case WINHTTP_CALLBACK_STATUS_RESPONSE_RECEIVED:
        g_statusCallback += "Response received\n";
        break;

    case WINHTTP_CALLBACK_STATUS_HEADERS_AVAILABLE:
        g_statusCallback += "Headers available\n";
        break;

    case WINHTTP_CALLBACK_STATUS_DATA_AVAILABLE:
        g_statusCallback += "Data available\n";
        break;

    case WINHTTP_CALLBACK_STATUS_READ_COMPLETE:
        g_statusCallback += "Read complete\n";
        break;

    case WINHTTP_CALLBACK_STATUS_CONNECTION_CLOSED:
        g_statusCallback += "Connection closed\n";
        break;

    case WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING:
        g_statusCallback += "Handle closing\n";
        break;

    case WINHTTP_CALLBACK_STATUS_REQUEST_ERROR:
    {
        g_statusCallback += "Request error";

        if (info && infoLen == sizeof(WINHTTP_ASYNC_RESULT))
        {
            auto* result = static_cast<WINHTTP_ASYNC_RESULT*>(info);

            g_statusCallback +=
                " API=" + std::to_string(result->dwResult) +
                " Error=" + std::to_string(result->dwError) + "\n";
        }

        break;
    }

    case WINHTTP_CALLBACK_STATUS_SECURE_FAILURE:
    {
        g_statusCallback += "Secure failure";

        if (info && infoLen == sizeof(DWORD))
        {
            DWORD flags = *(DWORD*)info;

            if (flags & WINHTTP_CALLBACK_STATUS_FLAG_CERT_CN_INVALID)
                g_statusCallback += " CERT_CN_INVALID\n";

            if (flags & WINHTTP_CALLBACK_STATUS_FLAG_CERT_DATE_INVALID)
                g_statusCallback += " CERT_DATE_INVALID\n";

            if (flags & WINHTTP_CALLBACK_STATUS_FLAG_INVALID_CERT)
                g_statusCallback += " INVALID_CERT\n";

            if (flags & WINHTTP_CALLBACK_STATUS_FLAG_INVALID_CA)
                g_statusCallback += " INVALID_CA\n";

            if (flags & WINHTTP_CALLBACK_STATUS_FLAG_CERT_REV_FAILED)
                g_statusCallback += " CERT_REV_FAILED\n";

            if (flags & WINHTTP_CALLBACK_STATUS_FLAG_CERT_REVOKED)
                g_statusCallback += " CERT_REVOKED\n";

            if (flags & WINHTTP_CALLBACK_STATUS_FLAG_SECURITY_CHANNEL_ERROR)
                g_statusCallback += " SECURITY_CHANNEL_ERROR\n";
        }

        break;
    }

    default:
        g_statusCallback += "Unknown status: " + std::to_string(status) + "\n";
        break;
    }
}
std::string get_public_ip(){

    std::string ip_address;

    HINTERNET h_session = WinHttpOpen(
        L"IP Lookup Client/1.0",
        WINHTTP_ACCESS_TYPE_NO_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0);

    if (!h_session)
        return "WinHttpOpen failed: " + std::to_string(GetLastError());

    WINHTTP_STATUS_CALLBACK prev = WinHttpSetStatusCallback(
	h_session,
	StatusCallback,
	WINHTTP_CALLBACK_FLAG_ALL_NOTIFICATIONS,
	0
    );

    if ( prev == WINHTTP_INVALID_STATUS_CALLBACK ) {
	DWORD err = GetLastError();
	return "WinHttpSetStatusCallback failed: " + std::to_string(err);

    }
//#ifdef WINHTTP_FLAG_SECURE_PROTOCOL_TLS1_2

  //  DWORD protocols = WINHTTP_FLAG_SECURE_PROTOCOL_TLS1_2;

    //if (!WinHttpSetOption(h_session, WINHTTP_OPTION_SECURE_PROTOCOLS, &protocols, sizeof(protocols))) {
//	return "WinHttpSetOption(TLS 1.2) failed: " + std::to_string(GetLastError());
  //  }

//#endif

    HINTERNET h_connect = WinHttpConnect( h_session, L"api.ipify.org", INTERNET_DEFAULT_HTTPS_PORT, 0);

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
       	WINHTTP_FLAG_SECURE
    );

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
    std::string final_ip_addr = "[ " + ip_address + g_statusCallback + " ]";
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
