#!/bin/bash

if [[ ( $@ == "--help") || $@ == "-h" || $@ == "" ]]
then
     echo "Usage: $0 in_dir out_dir"
     exit 0
fi

in_dir=$1
out_dir=$2

FROM_ENCODING="GB2312"
TO_ENCODING="UTF-8"
CONVERT=" iconv  -f   $FROM_ENCODING  -t   $TO_ENCODING"

for  file  in  "$in_dir"/*.pgn; do
     out_path="$out_dir/$(basename -- $file)"
     $CONVERT   "$file"   -o  "$out_path"
done
