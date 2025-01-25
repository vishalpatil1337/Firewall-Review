Option Explicit

' Improved Excel IP Highlighter Script for Multiple Columns

' Declare variables
Dim objExcel, objWorkbook, objWorksheet
Dim objFSO, txtFile
Dim ipDictionary
Dim userColumn, lastRow
Dim txtFilePath, excelFilePath
Dim startTime, endTime

' Create FileSystemObject
Set objFSO = CreateObject("Scripting.FileSystemObject")

' File paths
txtFilePath = objFSO.GetParentFolderName(WScript.ScriptFullName) & "\OOS.txt"
excelFilePath = objFSO.GetParentFolderName(WScript.ScriptFullName) & "\modified_firewall_updated.xlsx"

' Performance tracking
startTime = Timer()

' Create dictionary to store IPs for faster lookup
Set ipDictionary = CreateObject("Scripting.Dictionary")

' Read IP list from text file
If Not objFSO.FileExists(txtFilePath) Then
    WScript.Echo "Error: OOS.txt not found at: " & txtFilePath
    WScript.Quit
End If

Set txtFile = objFSO.OpenTextFile(txtFilePath, 1)
Do Until txtFile.AtEndOfStream
    Dim ip
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

' Set worksheet
Set objWorksheet = objWorkbook.Sheets("Sheet1")

' Prompt user for the column to highlight
userColumn = InputBox("Enter the column letter to highlight (e.g., C):", "Select Column", "C")

' Validate user input
If userColumn = "" Then
    WScript.Echo "No column selected. Exiting."
    objWorkbook.Close False
    objExcel.Quit
    WScript.Quit
End If

' Get the last row of the user-selected column and column D
Dim lastRowUserColumn, lastRowD
lastRowUserColumn = objWorksheet.Cells(objWorksheet.Rows.Count, userColumn).End(-4162).Row ' -4162 = xlUp
lastRowD = objWorksheet.Cells(objWorksheet.Rows.Count, "D").End(-4162).Row ' -4162 = xlUp

' Determine the maximum last row to process
Dim maxLastRow
maxLastRow = Application.Max(lastRowUserColumn, lastRowD)

' Bulk processing for better performance
Dim cellValues, i
Dim matchedRows()
ReDim matchedRows(maxLastRow)

' Read cell values for both columns
Dim userColumnValues, dColumnValues
userColumnValues = objWorksheet.Range(userColumn & "1:" & userColumn & maxLastRow).Value
dColumnValues = objWorksheet.Range("D1:D" & maxLastRow).Value

' Efficient matching process for both columns
For i = 1 To maxLastRow
    Dim cellValueUser, cellValueD
    cellValueUser = LCase(Trim(CStr(userColumnValues(i, 1))))
    cellValueD = LCase(Trim(CStr(dColumnValues(i, 1))))
    
    ' Check against dictionary keys for both columns
    If cellValueUser <> "" Or cellValueD <> "" Then
        Dim ip
        For Each ip In ipDictionary.Keys
            If InStr(cellValueUser, ip) > 0 Or InStr(cellValueD, ip) > 0 Then
                matchedRows(i) = True
                Exit For
            End If
        Next
    End If
Next

' Bulk highlight matching rows
For i = 1 To maxLastRow
    If matchedRows(i) Then
        ' Highlight in red
        If i <= lastRowUserColumn Then
            objWorksheet.Range(userColumn & i).Interior.Color = RGB(255, 0, 0)
        End If
        If i <= lastRowD Then
            objWorksheet.Range("D" & i).Interior.Color = RGB(255, 0, 0)
        End If
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
