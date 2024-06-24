# Firewall-Review
This Tool can be helpful during FIrewall Review Testing for checking CDE and OOS subnets from Source and Destination


Step 1 : Extract all Tables from Nipper and combine them in 1 excel file using move *.cve all-in-one.cve   
Step 2 : Use STAGE 3 Script to make tables in unique format     
Step 3 : Copy Firewall ruleset in Excel and pest the step 2 result there, also copy services and IP address from Nipper Report.         
Step 4 : Use the STAGE 2 script. Large lines cannot be copied and pasted, so they need to be handled manually.     
Step 5: You will see IPs and subnets in all Source & Destination fields. Use Firewall-review script to find CDE & OOS IPs and Subnets.     


# VBS SCRIPT - STAGE 1 : Find and Replace
```
Sub MultiFindNReplace()
'Update 20140722
Dim Rng As Range
Dim InputRng As Range, ReplaceRng As Range
xTitleId = "KutoolsforExcel"
Set InputRng = Application.Selection
Set InputRng = Application.InputBox("Original Range ", xTitleId, InputRng.Address, Type:=8)
Set ReplaceRng = Application.InputBox("Replace Range :", xTitleId, Type:=8)
Application.ScreenUpdating = False
For Each Rng In ReplaceRng.Columns(1).Cells
    InputRng.Replace what:=Rng.Value, replacement:=Rng.Offset(0, 1).Value, Lookat:=xlWhole
Next
Application.ScreenUpdating = True
End Sub

```

# VBS SCRIPT - STAGE 2 : Find and Replace (Updated Script)
```
Sub BulkReplace()
  Dim Rng As Range, SourceRng As Range, ReplaceRng As Range
  On Error Resume Next

  Set SourceRng = Application.InputBox("Source data:", "Bulk Replace", Application.Selection.Address, Type:=8)
  Err.Clear

  If Not SourceRng Is Nothing Then
  Set ReplaceRng = Application.InputBox("Replace range:", "Bulk Replace", Type:=8)
  Err.Clear
  If Not ReplaceRng Is Nothing Then
    Application.ScreenUpdating = False
    For Each Rng In ReplaceRng.Columns(1).Cells
      SourceRng.Replace what:=Rng.Value, replacement:=Rng.Offset(0, 1).Value
    Next
    Application.ScreenUpdating = True
  End If
  End If
End Sub
```

# VBS SCRIPT - STAGE 3 : Firewall Review : Tables to Groups (To remove multiple things and add Multiple IPs in unique Table

```
Sub CombineNames()
    Dim wsSource As Worksheet
    Dim wsOutput As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim tableDict As Object
    Dim tableKey As Variant
    Dim combinedNames As String
    
    ' Set source and output worksheets
    Set wsSource = ThisWorkbook.Sheets("Sheet1") ' Change "Sheet1" to the name of your source sheet
    Set wsOutput = ThisWorkbook.Sheets.Add
    
    ' Create dictionary to store combined names for each table
    Set tableDict = CreateObject("Scripting.Dictionary")
    
    ' Find last row in source sheet
    lastRow = wsSource.Cells(wsSource.Rows.Count, "A").End(xlUp).Row
    
    ' Loop through rows in source sheet
    For i = 2 To lastRow ' Assuming data starts from row 2 and headers are in row 1
        If Not tableDict.exists(wsSource.Cells(i, 1).Value) Then
            ' If table not found in dictionary, add it and initialize combinedNames
            tableDict.Add wsSource.Cells(i, 1).Value, wsSource.Cells(i, 2).Value
        Else
            ' If table found in dictionary, append name to combinedNames
            combinedNames = tableDict(wsSource.Cells(i, 1).Value)
            combinedNames = combinedNames & ", " & wsSource.Cells(i, 2).Value
            tableDict(wsSource.Cells(i, 1).Value) = combinedNames
        End If
    Next i
    
    ' Output results to new sheet
    wsOutput.Range("A1").Value = "Table"
    wsOutput.Range("B1").Value = "Name"
    i = 2
    For Each tableKey In tableDict.keys
        wsOutput.Cells(i, 1).Value = tableKey
        wsOutput.Cells(i, 2).Value = tableDict(tableKey)
        i = i + 1
    Next tableKey
    
    ' Adjust column widths for better visibility
    wsOutput.Columns("A:B").AutoFit


# VBS Maching With Colour IP - Using for Identifying CDE,OOS Subnets

    MsgBox "Combining names completed.", vbInformation
    
End Sub
```

# VBS Script - Colourful Matching

 ```
Sub HighlightIPMatches()
    Dim ws As Worksheet
    Dim rngIPs As Range
    Dim rngCheck As Range
    Dim cellIP As Range
    Dim cellCheck As Range
    Dim IP As String
    Dim checkValue As String
    
    ' Set the active worksheet
    Set ws = ActiveSheet
    
    ' Prompt user to select the range with IP addresses (K column)
    On Error Resume Next
    Set rngIPs = Application.InputBox("Select the range of IP addresses", "Select Range", Type:=8)
    If rngIPs Is Nothing Then Exit Sub
    Debug.Print "IP range selected: " & rngIPs.Address
    
    ' Prompt user to select the range to check (D column)
    Set rngCheck = Application.InputBox("Select the range to check against", "Select Range", Type:=8)
    If rngCheck Is Nothing Then Exit Sub
    Debug.Print "Check range selected: " & rngCheck.Address
    On Error GoTo 0
    
    ' Loop through each cell in the IP range
    For Each cellIP In rngIPs
        IP = Trim(cellIP.Value)
        If IP <> "" Then
            Debug.Print "Checking IP: " & IP
            ' Loop through each cell in the check range
            For Each cellCheck In rngCheck
                checkValue = cellCheck.Value
                ' Check if the IP is part of the string in the check range
                If InStr(1, checkValue, IP, vbTextCompare) > 0 Then
                    ' Highlight matching cells in red
                    cellIP.Interior.Color = RGB(255, 0, 0)
                    cellCheck.Interior.Color = RGB(255, 0, 0)
                    Debug.Print "Match found: " & IP & " in " & checkValue
                End If
            Next cellCheck
        End If
    Next cellIP
    
    ' Notify the user that the script has completed
    MsgBox "Highlighting complete"
End Sub


```
