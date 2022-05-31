import PyPDF2 as p2

PDFfile = open("pdfbig.pdf","rb")
pdfRead = p2.PdfFileReader(PDFfile)

print(pdfRead.documentInfo)
print(pdfRead.getNumPages())
print(pdfRead.getPage(1).extractText())

for i in range(0, pdfRead.getNumPages()):
    print(pdfRead.getPage(i).extractText())