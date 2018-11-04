# Input data

1. catalogue.xlsx has 11 columns.
2. pdfFiles folder has books in the format `BOOK_NO.<accessionNumber>.pdf` format where accessionNumber is the column 2 of catalogue.xlsx.
3. In our test data we have only two files 1246 and 1520 PDF. Their corresponding entries are made in catalogue.xlsx.

# Output expectation

1. We need to device an automatic bot to upload the PDF files to archive.org.
2. https://internetarchive.readthedocs.io/en/latest/ is the python library for bulk upload.

