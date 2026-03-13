param(
    [string]$PythonExe = "python",
    [switch]$SkipGenerate
)

$root = "E:\workfile\JAVA\NewAPI"
$generator = "E:\workfile\JAVA\NewAPI\scripts\generate_compare_manifests.py"
$compareScript = "E:\workfile\JAVA\NewAPI\scripts\compare_api.py"
$jobs = @(
    @{
        Name = "window_1"
        Manifest = "E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_1.json"
        Report = "E:\workfile\JAVA\NewAPI\docs\window_1_dynamic_compare_report.md"
    },
    @{
        Name = "window_2"
        Manifest = "E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_2.json"
        Report = "E:\workfile\JAVA\NewAPI\docs\window_2_dynamic_compare_report.md"
    },
    @{
        Name = "window_3"
        Manifest = "E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_3.json"
        Report = "E:\workfile\JAVA\NewAPI\docs\window_3_dynamic_compare_report.md"
    },
    @{
        Name = "window_4"
        Manifest = "E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_4.json"
        Report = "E:\workfile\JAVA\NewAPI\docs\window_4_dynamic_compare_report.md"
    }
)

Set-Location $root

if (-not $SkipGenerate) {
    Write-Host "Regenerating manifests from endpoint_case_library.json ..."
    & $PythonExe $generator
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Manifest generation failed. Stop launching compare windows."
        exit $LASTEXITCODE
    }
    Write-Host ""
}

foreach ($job in $jobs) {
    $command = @"
`$Host.UI.RawUI.WindowTitle = '$($job.Name)'
Write-Host 'Starting $($job.Name)...'
Set-Location '$root'
& $PythonExe '$compareScript' --manifest '$($job.Manifest)' --report '$($job.Report)'
Write-Host ''
Write-Host 'Finished $($job.Name). Report: $($job.Report)'
"@
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $command | Out-Null
    Write-Host "Started $($job.Name): $($job.Manifest)"
}

Write-Host ""
Write-Host "All four compare windows were launched."
Write-Host "After they all finish, run:"
Write-Host "python scripts/summarize_compare_reports.py --output docs/dynamic_compare_master_report_20260310.md"
