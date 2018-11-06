# v000.xls

Raw data given by CGV data entry operator.

# v001.xls

1. Corrected the entries running in multiple lines in a cell to a single line. (Done in both catalogues.)
2. Added categories at the column Q. (Done in both catalogues.)

# v001.tsv

The same as v001.xls but converted to tsv.

# v002.tsv

1. Remove nuktas and abnormal orthography. e.g. फ़ -> फ, ड़ -> ड, देवष्यॉचार्यतर्पण -> देवर्ष्याचार्यतर्पण, निझॅरणव्रतकथा -> निर्झरणव्रतकथा,  पञ्चाशद्वणॅसंचय -> पञ्चाशद्वर्णसंचय.
After these corrections, the SLP1 transliteration is allowed to be printed on screen.
2. Column F changed to from Sanskrit to English 'Paper'.

# v003.tsv

1. Correction in the marking of x for folio sizes. There is no possibility of a manuscript running in feet. So all ' have to be changed to ". Columns H and I are affected.

# v004.tsv

1. Conditions of MSS converted back to English. Column N.

# v005.tsv

1. Remove unnecessary H and : from Title, Author, Commentator, Scribe columns.
2. Convert Sr. No. and Accession No. to Roman alphanumeric.
3. Convert Vikrama Samvat and Shaka samvat.
4. Convert _ to --.

# v006.tsv
1. This is done by a separate script `python manualCorrection.py`.
2. Change the Sanskrit words from Additional Remarks column to Devanagari for uniformity.
3. 5th letter of each varga used instead of M.
