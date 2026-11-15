$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$taskRoot = 'C:\Projets\Tiktok - MrBallen\out\48-faid-evasion-helicoptere'
& ffmpeg -v error -y -i "$taskRoot\final.mp4" -vn -ar 16000 -ac 1 -c:a pcm_s16le "$taskRoot\_montage\audio-export.wav"
$recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine([System.Globalization.CultureInfo]::GetCultureInfo('fr-FR'))
$recognizer.LoadGrammar((New-Object System.Speech.Recognition.DictationGrammar))
$recognizer.SetInputToWaveFile("$taskRoot\_montage\audio-export.wav")
$segments = @()
while ($true) {
    try { $result = $recognizer.Recognize() } catch { if ($segments.Count -gt 0) { break } else { throw } }
    if ($null -eq $result) { break }
    $segments += [pscustomobject]@{ texte=$result.Text; confiance=$result.Confidence; debut=$result.Audio.AudioPosition.TotalSeconds; duree=$result.Audio.Duration.TotalSeconds }
}
$segments | ConvertTo-Json -Depth 5 | Set-Content "$taskRoot\_montage\transcription-windows.json" -Encoding UTF8
$segments | Format-Table -AutoSize
$recognizer.Dispose()


