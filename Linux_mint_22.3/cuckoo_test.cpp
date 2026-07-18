#include <windows.h>
#include <bcrypt.h>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <vector>
#include <stdexcept>

#pragma comment(lib, "bcrypt.lib")

std::string sha256File(const std::string& filename)
{
    std::ifstream file(filename, std::ios::binary);

    if (!file)
        throw std::runtime_error("Cannot open file");

    BCRYPT_ALG_HANDLE alg = nullptr;
    BCRYPT_HASH_HANDLE hashHandle = nullptr;

    DWORD objectSize = 0;
    DWORD resultSize = 0;

    BCryptOpenAlgorithmProvider(
        &alg,
        BCRYPT_SHA256_ALGORITHM,
        nullptr,
        0);

    BCryptGetProperty(
        alg,
        BCRYPT_OBJECT_LENGTH,
        (PUCHAR)&objectSize,
        sizeof(objectSize),
        &resultSize,
        0);

    std::vector<unsigned char> object(objectSize);

    BCryptCreateHash(
        alg,
        &hashHandle,
        object.data(),
        objectSize,
        nullptr,
        0,
        0);

    char buffer[8192];

    while (file.read(buffer, sizeof(buffer)) || file.gcount())
    {
        BCryptHashData(
            hashHandle,
            (PUCHAR)buffer,
            (ULONG)file.gcount(),
            0);
    }

    unsigned char digest[32];

    BCryptFinishHash(
        hashHandle,
        digest,
        sizeof(digest),
        0);

    BCryptDestroyHash(hashHandle);
    BCryptCloseAlgorithmProvider(alg, 0);

    std::stringstream ss;

    for (unsigned char c : digest)
    {
        ss << std::hex
           << std::setw(2)
           << std::setfill('0')
           << (int)c;
    }

    return ss.str();
}

int main(int argc, char* argv[])
{
    char* name = "C:\\Windows\\System32\\notepad.exe";

    std::string hash = sha256File(name);

    std::ofstream out("hash.txt");
    out << "SHA256: " << hash << "\n";
    out.close();

    STARTUPINFOA si{};
    PROCESS_INFORMATION pi{};

    si.cb = sizeof(si);

    char cmd[] = "notepad.exe hash.txt";

    if (CreateProcessA(
            nullptr,
            cmd,
            nullptr,
            nullptr,
            FALSE,
            0,
            nullptr,
            nullptr,
            &si,
            &pi))
    {
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    }
    else
    {
        std::cerr << "CreateProcess failed: "
                  << GetLastError()
                  << "\n";
    }

    return 0;
}
