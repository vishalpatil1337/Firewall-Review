Option Explicit

' Improved Excel IP Highlighter Script

' Declare variables
Dim objExcel, objWorkbook, objWorksheet
Dim objFSO, txtFile
Dim ipDictionary, ip
Dim userColumn, lastRow
Dim txtFilePath, excelFilePath
Dim startTime, endTime

' Create FileSystemObject
Set objFSO = CreateObject("Scripting.FileSystemObject")

' File paths
txtFilePath = objFSO.GetParentFolderName(WScript.ScriptFullName) & "\CDE.txt"
excelFilePath = objFSO.GetParentFolderName(WScript.ScriptFullName) & "\modified_firewall_updated.xlsx"

' Performance tracking
startTime = Timer()

' Create dictionary to store IPs for faster lookup
Set ipDictionary = CreateObject("Scripting.Dictionary")

' Read IP list from text file
If Not objFSO.FileExists(txtFilePath) Then
    WScript.Echo "Error: CDE.txt not found at: " & txtFilePath
    WScript.Quit
End If

Set txtFile = objFSO.OpenTextFile(txtFilePath, 1)
Do Until txtFile.AtEndOfStream
    ip = Trim(LCase(txtFile.ReadLine))
    If ip <> "" Then
        If Not ipDictionary.Exists(ip) Then
            ipDictionary.Add ip, True
        End If
    End If
Loop
txtFile.Close

' Create Excel application object
Set objExcel = CreateObject("Excel.Application")
objExcel.DisplayAlerts = False ' Suppress alerts
objExcel.ScreenUpdating = False ' Disable screen updating for performance
objExcel.Calculation = -4135 ' xlCalculationManual - Disable automatic calculations

On Error Resume Next

' Open the workbook
Set objWorkbook = objExcel.Workbooks.Open(excelFilePath)
If Err.Number <> 0 Then
    WScript.Echo "Error opening workbook: " & Err.Description
    objExcel.Quit
    WScript.Quit
End If

' Prompt user for the column to highlight
userColumn = InputBox("Enter the column letter to highlight (e.g., C or D):", "Select Column", "C")

' Validate user input
If userColumn = "" Then
    WScript.Echo "No column selected. Exiting."
    objWorkbook.Close False
    objExcel.Quit
    WScript.Quit
End If

' Set worksheet and define range
Set objWorksheet = objWorkbook.Sheets("Sheet1")
lastRow = objWorksheet.Cells(objWorksheet.Rows.Count, userColumn).End(-4162).Row ' -4162 = xlUp

' Bulk processing for better performance
Dim cellValues, i
Dim matchedRows()
ReDim matchedRows(lastRow)

' Read cell values once
cellValues = objWorksheet.Range(userColumn & "1:" & userColumn & lastRow).Value

' Efficient matching process
For i = 1 To UBound(cellValues, 1)
    Dim cellValue, matchFound
    cellValue = LCase(Trim(CStr(cellValues(i, 1))))
    
    ' Check against dictionary keys
    If cellValue <> "" Then
        For Each ip In ipDictionary.Keys
            If InStr(cellValue, ip) > 0 Then
                matchedRows(i) = True
                Exit For
            End If
        Next
    End If
Next

' Bulk highlight matching rows
For i = 1 To UBound(matchedRows)
    If matchedRows(i) Then
        objWorksheet.Range(userColumn & i).Interior.Color = RGB(0, 255, 0) ' Green
    End If
Next

' Save and close workbook
objWorkbook.Save
objWorkbook.Close

' Reset Excel settings
objExcel.Calculation = -4105 ' xlCalculationAutomatic
objExcel.ScreenUpdating = True
objExcel.DisplayAlerts = True

' Quit Excel
objExcel.Quit

' Performance tracking
endTime = Timer()

' Display completion message with performance info
WScript.Echo "Highlighting complete!" & vbNewLine & _
             "Processing Time: " & Round(endTime - startTime, 2) & " seconds"

' Clean up objects
Set ipDictionary = Nothing
Set objFSO = Nothing
Set objExcel = Nothing
Set objWorkbook = Nothing
Set objWorksheet = Nothing
