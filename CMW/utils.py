import os

import xlwt
from django.http import HttpResponse

from CMW import settings


def export_xls(name_object, file_name, name_sheet, columns, rows):
    response = HttpResponse(content_type='application/ms-excel')

    response['Content-Disposition'] = 'attachment; filename=' + file_name + name_object + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(name_sheet)

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.easyxf('font: bold 1,height 250;')
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.easyxf('font: height 230;')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

