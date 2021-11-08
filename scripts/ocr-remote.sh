echo "Make sure the raw directory exists"
mkdir -p raw/

echo "Cleanup the raw directory"
rm -r raw/*

echo "Download URL: $1"
curl --cipher 'DEFAULT:!DH' $1 --output raw/doc.pdf

echo "Transform the PDF to PNG images"
pdftoppm raw/doc.pdf raw/images -png
rename images- images-00 raw/images-?.png
rename images- images-0 raw/images-??.png 2>/dev/null

echo "Run OCR for each image and refine the results"
tesseract raw/images-001.png stdout -l pol | ./scripts/refine-ocr.py --first-page > raw/page.md
shopt -s extglob
for filename in raw/images-!(001.png); do
    tesseract $filename stdout -l pol | ./scripts/refine-ocr.py >> raw/page.md
done