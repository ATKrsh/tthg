# PowerShell script to unblock and sign TTHG executable for Windows Smart App Control / Defender
$ErrorActionPreference = "SilentlyContinue"

$DistFolder = Join-Path $PSScriptRoot "dist"
$Exes = Get-ChildItem -Path $DistFolder -Filter "*.exe" -Recurse

Write-Host "1. Unblocking executables from SmartScreen Zone.Identifier..." -ForegroundColor Cyan
foreach ($exe in $Exes) {
    Unblock-File -Path $exe.FullName
    Write-Host "Unblocked: $($exe.FullName)" -ForegroundColor Green
}

Write-Host "2. Checking / Creating Self-Signed Code Signing Certificate..." -ForegroundColor Cyan
$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert | Where-Object { $_.Subject -like "*TTHG Code Signing*" } | Select-Object -First 1

if (-not $cert) {
    Write-Host "Generating TTHG Code Signing Certificate..." -ForegroundColor Yellow
    $cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=TTHG Code Signing Cert" -CertStoreLocation Cert:\CurrentUser\My
}

if ($cert) {
    Write-Host "3. Signing executables with Authenticode Signature..." -ForegroundColor Cyan
    foreach ($exe in $Exes) {
        Set-AuthenticodeSignature -FilePath $exe.FullName -Certificate $cert | Out-Null
        Write-Host "Signed: $($exe.Name)" -ForegroundColor Green
    }
}

Write-Host "Done! All executables in dist/ are unblocked and signed." -ForegroundColor Green
