# make dataset after stack processor completes

export PROCESSING_START=$(date +%FT%T)
# it also assumes existence of
# _context.txt with non-empty member "localize_urls" as list
# dirs: ./merged, ./reference and ./secondarys
python ./make_dataset.py -b "34.6002832,34.6502392,-79.0801608,-78.9705888"
