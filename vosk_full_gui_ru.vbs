Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "C:\VOSK\vosk_full_gui_ru.bat" & Chr(34), 0
Set WshShell = Nothing