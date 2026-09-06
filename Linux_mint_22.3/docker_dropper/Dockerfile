FROM ubuntu:24.04

RUN apt update && apt install -y g++ 

WORKDIR /src

COPY . /src

RUN g++ main.cpp -o main.exe

CMD ["./main.exe"]
