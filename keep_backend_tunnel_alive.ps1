while ($true) {
    Write-Host "Starting Localtunnel for Backend..."
    npx localtunnel --port 8000 --subdomain nadabrahma-backend-1910
    Write-Host "Backend Localtunnel crashed. Restarting in 2 seconds..."
    Start-Sleep -Seconds 2
}
