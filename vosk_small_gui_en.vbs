Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "C:\VOSK\vosk_small_gui_en.bat" & Chr(34), 0
Set WshShell = Nothing