import xlwt
from django.http import HttpResponse


def export_xls(name_object, file_name, name_sheet, columns, rows):
    """Скачивание .xls файла"""
    response = HttpResponse(content_type='application/vnd.ms-excel')
    filename = '{}{}.xls'.format(file_name, name_object)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(name_sheet)
    row_num = 0

    font_style = xlwt.easyxf('font: bold 1,height 220;')
    font_style.font.bold = True

    for col_num in range(len(columns)):
        a = str(columns[col_num])
        if col_num == 0:
            ws.col(col_num).width = len(a) * 1200
        elif col_num == 5:
            ws.col(col_num).width = len(a) * 800
        else:
            ws.col(col_num).width = len(a) * 367
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.easyxf('font: height 210;')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            cwidth = ws.col(col_num).width

            ws.write(row_num, col_num, row[col_num], font_style, )
    wb.save(response)
    return response
