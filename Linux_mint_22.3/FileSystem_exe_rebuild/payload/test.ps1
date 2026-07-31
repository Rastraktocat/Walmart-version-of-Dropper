$uri = "https://api.ipify.org"

if ($PSVersionTable.PSVersion.Major -ge 3) {
	try {
		$response = Invoke-WebRequest -Uri $uri -UseBasicParsing
		$response.Content
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
	}
	catch {
		Write-Host "WebClient failed."
		Write-Host $_.Exception.Message
	}
}
