#!/bin/bash
fitspath="$1"
thumbpath="$2"

if ! [ -d "$2" ]
then
	thumbpath="$fitspath/Thumbnails/"
	if ! [ -d "$thumbpath" ]
	then
		echo "Creating $thumbpath"
		mkdir "$thumbpath"
	fi
fi

for file in "$fitspath/"*.fits; do [ -f "$thumbpath/"$(basename ${file%.*}).jpg ] && echo "File exist" || (convert "$file" -linear-stretch 1x1 -resize 56%  "$thumbpath/$(basename ${file%.*}).jpg" && echo "Created") ; done;
