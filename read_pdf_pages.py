# coding:utf-8
import os
from PyPDF2 import PdfFileReader


def read_pdf_pages():
    list_path = r'F:\桌面\Desktop\待打印\待打印\新建文件夹'
    all_pages = 0

    for file in os.listdir(list_path):
        full_path = list_path + '\\' + file
        reader = PdfFileReader(full_path)

        page = reader.getNumPages()
        print(file, page)

        pages = str(page).split()[-1]
        # print(pages)
        all_pages += int(pages)
    print(all_pages)


if __name__ == '__main__':
    read_pdf_pages()
