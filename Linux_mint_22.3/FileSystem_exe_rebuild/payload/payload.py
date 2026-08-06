import ctypes
from ctypes import wintypes
import os
import subprocess


winhttp = ctypes.WinDLL("winhttp.dll")

STATUS = []


def status(msg):
    STATUS.append(msg)
    print(msg)


# Constants
WINHTTP_ACCESS_TYPE_NO_PROXY = 1
WINHTTP_NO_PROXY_NAME = None
WINHTTP_NO_PROXY_BYPASS = None

WINHTTP_FLAG_SECURE = 0x00800000

WINHTTP_QUERY_STATUS_CODE = 19
WINHTTP_QUERY_FLAG_NUMBER = 0x20000000

WINHTTP_OPTION_SECURE_PROTOCOLS = 84
WINHTTP_FLAG_SECURE_PROTOCOL_TLS1_2 = 0x00000800


# Function prototypes
winhttp.WinHttpOpen.restype = wintypes.HANDLE

winhttp.WinHttpConnect.restype = wintypes.HANDLE

winhttp.WinHttpOpenRequest.restype = wintypes.HANDLE

winhttp.WinHttpSendRequest.restype = wintypes.BOOL

winhttp.WinHttpReceiveResponse.restype = wintypes.BOOL

winhttp.WinHttpQueryHeaders.restype = wintypes.BOOL

winhttp.WinHttpQueryDataAvailable.restype = wintypes.BOOL

winhttp.WinHttpReadData.restype = wintypes.BOOL

winhttp.WinHttpCloseHandle.restype = wintypes.BOOL


def get_error():
    return ctypes.GetLastError()


def get_public_ip():

    ip = ""

    session = winhttp.WinHttpOpen(
        "IP Lookup Client/1.0",
        WINHTTP_ACCESS_TYPE_NO_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0
    )

    if not session:
        return "WinHttpOpen failed: {}".format(get_error())

    status("Session opened")

    # Force TLS 1.2
    protocols = wintypes.DWORD(WINHTTP_FLAG_SECURE_PROTOCOL_TLS1_2)

    winhttp.WinHttpSetOption(
        session,
        WINHTTP_OPTION_SECURE_PROTOCOLS,
        ctypes.byref(protocols),
        ctypes.sizeof(protocols)
    )

    status("TLS 1.2 enabled")

    connect = winhttp.WinHttpConnect(
        session,
        "api.ipify.org",
        443,
        0
    )

    if not connect:
        return "WinHttpConnect failed: {}".format(get_error())

    status("Connected to server")

    request = winhttp.WinHttpOpenRequest(
        connect,
        "GET",
        "/",
        None,
        None,
        None,
        WINHTTP_FLAG_SECURE
    )

    if not request:
        return "WinHttpOpenRequest failed: {}".format(get_error())

    status("Request created")

    if not winhttp.WinHttpSendRequest(
        request,
        None,
        0,
        None,
        0,
        0,
        0
    ):
        return "WinHttpSendRequest failed: {}".format(get_error())

    status("Request sent")

    if not winhttp.WinHttpReceiveResponse(
        request,
        None
    ):
        return "WinHttpReceiveResponse failed: {}".format(get_error())

    status("Response received")


    # HTTP status code
    http_status = wintypes.DWORD()
    size = wintypes.DWORD(ctypes.sizeof(http_status))

    if not winhttp.WinHttpQueryHeaders(
        request,
        WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
        None,
        ctypes.byref(http_status),
        ctypes.byref(size),
        None
    ):
        return "WinHttpQueryHeaders failed: {}".format(get_error())


    if http_status.value != 200:
        return "HTTP status code: {}".format(http_status.value)


    status("Headers available")


    while True:

        available = wintypes.DWORD()

        if not winhttp.WinHttpQueryDataAvailable(
            request,
            ctypes.byref(available)
        ):
            return "WinHttpQueryDataAvailable failed: {}".format(get_error())


        if available.value == 0:
            break


        buffer = ctypes.create_string_buffer(
            available.value
        )

        read = wintypes.DWORD()

        if not winhttp.WinHttpReadData(
            request,
            buffer,
            available.value,
            ctypes.byref(read)
        ):
            return "WinHttpReadData failed: {}".format(get_error())


        ip += buffer.raw[:read.value].decode()


    winhttp.WinHttpCloseHandle(request)
    winhttp.WinHttpCloseHandle(connect)
    winhttp.WinHttpCloseHandle(session)


    if not ip:
        return "Received empty response"

    return ip.strip()



def file_setup():

    result = get_public_ip()

    output = "[ {} \n\n{} ]".format(
        result,
        "\n".join(STATUS)
    )

    path = r"C:\Users\Administrator\Downloads\file_output.txt"

    with open(path, "w") as f:
        f.write(output)

    print("Written:", path)



def pop_out_file():

    path = r"C:\Users\Administrator\Downloads\file_output.txt"

    if os.path.exists(path):
        subprocess.Popen(
            [
                r"C:\Windows\System32\notepad.exe",
                path
            ]
        )
    else:
        print("File missing")


if __name__ == "__main__":
    file_setup()
    pop_out_file()
