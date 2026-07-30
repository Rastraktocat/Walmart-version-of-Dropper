#include<windows.h>
#include<winhttp.h>
#include<fstream>
#include<stdio.h>
#include<cstdlib>
#include<iostream>

void file_setup(){

    std::string ip_address = getPublicIP();

    std::string filepath = "C:\\Users\\Administrator\\Downloads\\file_output";

    std::ofstream _file(filepath);
    _file.write(ip_address);

}

void pop_out_file(){

    STARTUPINFOW si{};
    PROCESS_INFORMATION pi{};
    si.cb = sizeof(si);

    int result = CreateProcessW(L"C:\\Users\\Administrator\\Downloads\\file_output", NULL, nullptr, nullptr, FALSE, 0, nullptr, nullptr, &si, &pi);
    if (result == 0) {
        std::cout << "CreateProcess failed.";
    }
}

int main(){

    file_setup();
    pop_out_file();

}
