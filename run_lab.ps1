param (
    [string]$LabDataDir = $env:LAB_DATA
)

if (-not $LabDataDir) {
    Write-Host "Vui long cung cap thu muc lab_data!" -ForegroundColor Red
    Write-Host "Cach dung: .\run_lab.ps1 -LabDataDir 'duong_dan_den_lab_data'"
    exit 1
}

$env:LAB_DATA = $LabDataDir
$PYTHON = "C:\Users\HP\anaconda3\envs\cv_robotics_lab21\python.exe"

Write-Host "=== BƯỚC 1: KIỂM TRA DỮ LIỆU ===" -ForegroundColor Cyan
& $PYTHON scripts/check_data.py --lab-data-root "$LabDataDir"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Kiem tra du lieu that bai!" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== BƯỚC 2: CHẠY TRACKING CHO 5 VIDEO ===" -ForegroundColor Cyan
& $PYTHON scripts/auto_run_lab.py --lab-data-root "$LabDataDir" --out runs/nop_bai --device cpu
if ($LASTEXITCODE -ne 0) {
    Write-Host "Chay tracking that bai!" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== BƯỚC 3: ĐÁNH GIÁ SỐ LIỆU VIDEO_1 (HOTA, MOTA, IDF1) ===" -ForegroundColor Cyan
& $PYTHON scripts/evaluate_practice.py --trackeval-root TrackEval --lab-data-root "$LabDataDir" --submission runs/nop_bai/video_1.txt --run-name nhom_video1

Write-Host "`n=== HOÀN TẤT TOÀN BỘ TIẾN TRÌNH ===" -ForegroundColor Green
Write-Host "Cac file ket qua da duoc luu vao thu muc: runs/nop_bai/"
Write-Host "Bao cao da duoc chuan bi san tai: submission_template/BAO_CAO.md"
