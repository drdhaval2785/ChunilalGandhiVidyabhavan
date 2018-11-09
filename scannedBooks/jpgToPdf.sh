#Convert spaces to underscore (for easier handling in bash)
#https://stackoverflow.com/questions/1806868/linux-replacing-spaces-in-the-file-names
# for file in *; do mv "$file" $(echo $file | tr ' ' '_') ; done

#Convert to PDF
#https://stackoverflow.com/questions/24051572/convert-images-to-pdfs-in-subdirectories
#find . -type d | while read d; do echo $d; magick "${d}"/*.jpg ../pdfBooks/"${d##*/}.pdf"; done

# Compress the PDF. Currently too bulky.
find . -type d | while read d; do echo $d; magick "${d}"/*.jpg -quality 30 ../compressedPdfFiles/"${d##*/}.pdf"; done
