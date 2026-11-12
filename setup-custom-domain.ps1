<#
.SYNOPSIS
    Configures the custom local development domain "http://api-security.local" for
    the AI-Driven API Security Assessment and Vulnerability Detection System.

.DESCRIPTION
    This script maps "api-security.local" to 127.0.0.1 in the Windows hosts file
    (C:\Windows\System32\drivers\etc\hosts) and flushes the local DNS resolver cache.
    Requires Administrator privileges to modify the hosts file.
#>

# 1. Check for Administrator Privileges
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[!] Administrator privileges are required to edit the Windows hosts file." -ForegroundColor Yellow
    Write-Host "[*] Requesting elevation..." -ForegroundColor Cyan
    try {
        Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
        exit 0
    } catch {
        Write-Host "[-] Elevation cancelled or failed. Please run PowerShell as Administrator and execute this script." -ForegroundColor Red
        exit 1
    }
}

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " AI-DRIVEN API SECURITY ASSESSMENT SYSTEM - DOMAIN CONFIGURATION" -ForegroundColor White
Write-Host " Preferred Domain: http://api-security.local" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$domainEntry = "127.0.0.1 api-security.local"

# 2. Check if already configured
$hostsContent = Get-Content -Path $hostsPath -Raw -ErrorAction Stop

if ($hostsContent -match "api-security\.local") {
    Write-Host "[+] Domain 'api-security.local' is ALREADY configured in: $hostsPath" -ForegroundColor Green
} else {
    Write-Host "[*] Adding entry to Windows hosts file..." -ForegroundColor Cyan
    $newEntry = "`r`n# Custom local domain for AI-Driven API Security Assessment System`r`n127.0.0.1 api-security.local`r`n"
    Add-Content -Path $hostsPath -Value $newEntry -Encoding ASCII
    Write-Host "[+] Successfully added '127.0.0.1 api-security.local' to hosts file!" -ForegroundColor Green
}

# 3. Flush DNS resolver cache
Write-Host "[*] Flushing Windows DNS resolver cache..." -ForegroundColor Cyan
ipconfig /flushdns | Out-Null
Write-Host "[+] Windows DNS cache flushed successfully." -ForegroundColor Green

# 4. Verify resolution
Write-Host "[*] Verifying domain resolution..." -ForegroundColor Cyan
try {
    $ip = [System.Net.Dns]::GetHostAddresses("api-security.local")
    Write-Host "[+] SUCCESS: 'api-security.local' resolves to: $($ip.IPAddressToString)" -ForegroundColor Green
} catch {
    Write-Host "[!] Note: Close and reopen your browser to ensure fresh DNS resolution." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " You can now open your browser and navigate to:" -ForegroundColor White
Write-Host " -> http://api-security.local" -ForegroundColor Green
Write-Host ""
Write-Host " (Fallback addresses: http://localhost and http://localhost:5173)" -ForegroundColor Gray
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
