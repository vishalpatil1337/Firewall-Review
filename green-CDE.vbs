Dim objExcel, objWorkbook, objWorksheet
Dim rngC, cell
Dim ipList, ip
Dim matchFound, txtFilePath, excelFilePath, userColumn, lastRow

' File paths
txtFilePath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\CDE.txt"
excelFilePath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\modified_firewall_updated.xlsx"

' Create Excel application object
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False  ' Run in the background

On Error Resume Next

' Open the workbook
Set objWorkbook = objExcel.Workbooks.Open(excelFilePath)
If Err.Number <> 0 Then
    WScript.Echo "Error opening workbook: " & Err.Description
    objExcel.Quit
    WScript.Quit
End If

Set objWorksheet = objWorkbook.Sheets("Sheet1")

' Prompt user for the column to highlight
userColumn = InputBox("Enter the column letter to highlight (e.g., C or D):", "Select Column", "C")

' Validate user input
If userColumn = "" Then
    WScript.Echo "No column selected. Exiting."
    objWorkbook.Close False
    objExcel.Quit
    WScript.Quit
End If

' Define the range based on user input
lastRow = objWorksheet.Cells(objWorksheet.Rows.Count, userColumn).End(-4162).Row ' -4162 = xlUp
Set rngC = objWorksheet.Range(userColumn & "1:" & userColumn & lastRow)

' Read the content of the text file
ipList = ""
Set fso = CreateObject("Scripting.FileSystemObject")
If fso.FileExists(txtFilePath) Then
    Set txtFile = fso.OpenTextFile(txtFilePath, 1)
    Do Until txtFile.AtEndOfStream
        ip = txtFile.ReadLine
        ipList = ipList & LCase(ip) & "|" ' Convert to lowercase
    Loop
    txtFile.Close
Else
    WScript.Echo "CDE.txt not found at: " & txtFilePath
    objWorkbook.Close False
    objExcel.Quit
    WScript.Quit
End If

' Remove trailing pipe character
If Right(ipList, 1) = "|" Then ipList = Left(ipList, Len(ipList) - 1)

' Loop through the selected range and highlight matches
For Each cell In rngC
    matchFound = False
    For Each ip In Split(ipList, "|")
        If InStr(LCase(cell.Value), Trim(ip)) > 0 Then ' Convert cell value to lowercase
            matchFound = True
            Exit For
        End If
    Next
    If matchFound Then cell.Interior.Color = RGB(0, 255, 0) ' Green
Next

' Save and close workbook
objWorkbook.Save
objWorkbook.Close

' Quit Excel
objExcel.Quit

WScript.Echo "Highlighting complete!"
