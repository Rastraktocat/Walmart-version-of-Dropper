$client = [Net.Sockets.TcpClient]::new("127.0.0.1", 8080)
$stream = $client.GetStream()

$message = "Dropper run"
$data = [Text.Encoding]::UTF8.GetBytes($message)

$stream.Write($data, 0, $data.Length)

$stream.Close()
$client.Close()
