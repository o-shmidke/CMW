import os

import xlwt
from django.http import HttpResponse

from CMW import settings


def export_xls(name_object, file_name, name_sheet, columns, rows):
    response = HttpResponse(content_type='application/ms-excel')
    filename = '{}_{}.xls'.format(file_name, name_object)
    # response['Content-Disposition'] = 'attachment; filename=' + file_name + name_object + '.xls'
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(name_sheet)
    # ws.set_column(50, 50, 1)
    # Sheet header, first row
    row_num = 0

    font_style = xlwt.easyxf('font: bold 1,height 220;')
    font_style.font.bold = True

    for col_num in range(len(columns)):
        a = str(columns[col_num])
        # if (len(a) * 367) > cwidth:

        if col_num == 0:
            ws.col(col_num).width = len(a) * 1200
        elif col_num == 5:
            ws.col(col_num).width = len(a) * 800
        else:
            ws.col(col_num).width = len(a) * 367
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.easyxf('font: height 210;')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            cwidth = ws.col(col_num).width

            ws.write(row_num, col_num, row[col_num], font_style, )
    wb.save(response)
    return response
