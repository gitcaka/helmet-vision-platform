$PythonExe = 'D:\software\miniconda\envs\py13\python.exe'

if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "未找到 py13 解释器：$PythonExe"
}

& $PythonExe (Join-Path $PSScriptRoot 'app.py')
exit $LASTEXITCODE
