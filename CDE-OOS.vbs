Option Explicit

' Helper function to check if IP matches any in the list
Function CheckIPInList(ip, ipList)
    Dim result(1), i, listIP
    result(0) = False  ' Match found
    result(1) = ""     ' Matched IP/subnet
    
    For i = 0 To UBound(ipList)
        listIP = Trim(ipList(i))
        ' First try exact match
        If LCase(ip) = LCase(listIP) Then
            result(0) = True
            result(1) = listIP
            Exit For
        End If
        ' Then try contains match for subnets
        If InStr(1, LCase(ip), LCase(listIP), vbTextCompare) > 0 Then
            result(0) = True
            result(1) = listIP
            Exit For
        End If
    Next
    
    CheckIPInList = result
End Function

Dim objExcel, objWorkbook, objSheet
Dim wsResults
Dim cell, cdeIPs, oosIPs
Dim currentPath
Dim txtFilePathCDE, txtFilePathOOS, excelFilePath
Dim lastRow, i
Dim fso, objFile, strLine

' Create FileSystemObject for file operations
Set fso = CreateObject("Scripting.FileSystemObject")

' Get current script directory
currentPath = fso.GetParentFolderName(WScript.ScriptFullName) & "\"
txtFilePathCDE = currentPath & "CDE.txt"
txtFilePathOOS = currentPath & "OOS.txt"
excelFilePath = currentPath & "modified_firewall_updated.xlsx"

' Verify files exist
If Not fso.FileExists(txtFilePathCDE) Then
    WScript.Echo "Error: CDE.txt not found in " & currentPath
    WScript.Quit
End If

If Not fso.FileExists(txtFilePathOOS) Then
    WScript.Echo "Error: OOS.txt not found in " & currentPath
    WScript.Quit
End If

If Not fso.FileExists(excelFilePath) Then
    WScript.Echo "Error: modified_firewall_updated.xlsx not found in " & currentPath
    WScript.Quit
End If

' Create Excel Objects
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = True

' Open workbook
Set objWorkbook = objExcel.Workbooks.Open(excelFilePath)
Set objSheet = objWorkbook.Sheets("Sheet1")

' Create new results sheet
On Error Resume Next
objWorkbook.Sheets("Analysis_Results").Delete
On Error GoTo 0

Set wsResults = objWorkbook.Sheets.Add
wsResults.Name = "Analysis_Results"

' Set up headers
wsResults.Cells(1, 1).Value = "Rule ID"           ' Column A
wsResults.Cells(1, 2).Value = "Source"            ' Column B
wsResults.Cells(1, 3).Value = "Destination"       ' Column C
wsResults.Cells(1, 4).Value = "Port"              ' Column D
wsResults.Cells(1, 5).Value = "Protocol"          ' Column E
wsResults.Cells(1, 6).Value = "Action"            ' Column F
wsResults.Cells(1, 8).Value = "Match Type"        ' Column H
wsResults.Cells(1, 9).Value = "Matched Source"    ' Column I
wsResults.Cells(1, 10).Value = "Matched Dest"     ' Column J

' Format headers
With wsResults.Range("A1:J1")
    .Font.Bold = True
    .Interior.Color = RGB(200, 200, 200)
End With

' Read CDE and OOS IPs/subnets
cdeIPs = ReadFileToArray(txtFilePathCDE)
oosIPs = ReadFileToArray(txtFilePathOOS)

' Get last row of source data
lastRow = objSheet.Cells(objSheet.Rows.Count, "C").End(-4162).Row

' Process each row
Dim resultRow: resultRow = 2
Dim sourceIP, destIP
Dim sourceCDEMatch, sourceOOSMatch, destCDEMatch, destOOSMatch

For i = 2 To lastRow
    sourceIP = Trim(objSheet.Cells(i, "C").Value)
    destIP = Trim(objSheet.Cells(i, "D").Value)
    
    If sourceIP <> "" And destIP <> "" Then
        ' Check both source and destination against both CDE and OOS lists
        sourceCDEMatch = CheckIPInList(sourceIP, cdeIPs)
        sourceOOSMatch = CheckIPInList(sourceIP, oosIPs)
        destCDEMatch = CheckIPInList(destIP, cdeIPs)
        destOOSMatch = CheckIPInList(destIP, oosIPs)
        
        ' Only process if we have CDE to OOS or OOS to CDE
        If (sourceCDEMatch(0) And destOOSMatch(0)) Or (sourceOOSMatch(0) And destCDEMatch(0)) Then
            ' Copy original rule data
            wsResults.Cells(resultRow, "A").Value = objSheet.Cells(i, "A").Value
            wsResults.Cells(resultRow, "B").Value = sourceIP
            wsResults.Cells(resultRow, "C").Value = destIP
            wsResults.Cells(resultRow, "D").Value = objSheet.Cells(i, "E").Value
            wsResults.Cells(resultRow, "E").Value = objSheet.Cells(i, "F").Value
            wsResults.Cells(resultRow, "F").Value = objSheet.Cells(i, "G").Value
            
            ' Set match type
            If sourceCDEMatch(0) And destOOSMatch(0) Then
                wsResults.Cells(resultRow, "H").Value = "CDE to OOS"
                wsResults.Cells(resultRow, "I").Value = sourceCDEMatch(1)
                wsResults.Cells(resultRow, "J").Value = destOOSMatch(1)
            ElseIf sourceOOSMatch(0) And destCDEMatch(0) Then
                wsResults.Cells(resultRow, "H").Value = "OOS to CDE"
                wsResults.Cells(resultRow, "I").Value = sourceOOSMatch(1)
                wsResults.Cells(resultRow, "J").Value = destCDEMatch(1)
            End If
            
            resultRow = resultRow + 1
        End If
    End If
Next

' Autofit columns
wsResults.Columns("A:J").AutoFit

' Save and cleanup
objWorkbook.Save
objWorkbook.Close
objExcel.Quit

Set wsResults = Nothing
Set objWorkbook = Nothing
Set objExcel = Nothing
Set fso = Nothing

WScript.Echo "Analysis complete!"

' Helper function to read file into array
Function ReadFileToArray(filePath)
    Dim content, tempLine
    content = ""
    Set objFile = fso.OpenTextFile(filePath, 1)
    
    Do Until objFile.AtEndOfStream
        tempLine = Trim(objFile.ReadLine)
        If tempLine <> "" Then
            content = content & tempLine & "|"
        End If
    Loop
    objFile.Close
    
    If Right(content, 1) = "|" Then content = Left(content, Len(content) - 1)
    ReadFileToArray = Split(content, "|")
End Function