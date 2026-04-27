for f in *.jpg; do
	out="compressed_$f"
	convert "$f" -quality 10% "$out"
done

