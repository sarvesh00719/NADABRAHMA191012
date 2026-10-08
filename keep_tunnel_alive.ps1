while ($true) {
    Write-Host "Starting Localtunnel for Gradio..."
    npx localtunnel --port 7860 --subdomain nadabrahma-gradio-1910
    Write-Host "Localtunnel crashed. Restarting in 2 seconds..."
    Start-Sleep -Seconds 2
}
