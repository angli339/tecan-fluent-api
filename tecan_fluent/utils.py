#
# Row/Col Name/Index conversion
#

def i_row_to_rowname(i_row):
    return "ABCDEFGH"[i_row]

def rowname_to_i_row(rowname):
    return "ABCDEFGH".index(rowname)

def i_col_row_to_wellname96(i_col: int, i_row: int):
    rowname = i_row_to_rowname(i_row)
    colname = str(i_col + 1)
    return rowname + colname

def wellname96_to_i_col_row(wellname: str):
    rowname = wellname[0]
    colname = wellname[1:]
    i_row = rowname_to_i_row(rowname)
    i_col = int(colname) - 1
    return i_col, i_row

