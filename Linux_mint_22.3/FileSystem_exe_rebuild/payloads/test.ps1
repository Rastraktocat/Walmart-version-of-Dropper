$uri = "https://api.ipify.org"
$path = "C:\Users\Administrator\Downloads\public_ip.txt"

if ($PSVersionTable.PSVersion.Major -ge 3) {
	try {
		$response = Invoke-WebRequest -Uri $uri -UseBasicParsing
		$response.Content
		$ip | Out-File -FilePath $path -Encoding Ascii
		echo $ip
		Write-Host $ip
		notepad $path
	}
	catch {
		Write-Host "Invoke WebRequest failed."
		Write-Host $_.Exception.Message
	}
}
else {
	try {
		$client = New-Object System.Net.WebClient
		$client.DownloadString($uri)
		$client | Out-File -FilePath $path -Encoding Ascii
		echo $ip
		Write-Host $ip
	}
	catch {
		Write-Host "WebClient failed."
		Write-Host $_.Exception.Message
	}
}
