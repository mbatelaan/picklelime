#!/bin/bash

lists=()

for f in meson*.lst; do
    [[ "$f" == *.common.lst ]] && continue
    lists+=("$f")
done

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

# Extract identifiers from the first list
grep -oE 'qcdsf\.[0-9]+\.[0-9]+' "${lists[0]}" \
    | sed 's/qcdsf\.//' \
    | sort -u > "$tmpdir/common"

# Intersect with identifiers from every other list
for list in "${lists[@]:1}"; do
    grep -oE 'qcdsf\.[0-9]+\.[0-9]+' "$list" \
        | sed 's/qcdsf\.//' \
        | sort -u > "$tmpdir/current"

    comm -12 "$tmpdir/common" "$tmpdir/current" > "$tmpdir/new_common"
    mv "$tmpdir/new_common" "$tmpdir/common"
done

echo "Common identifiers:"
cat "$tmpdir/common"

echo
echo "Number of common identifiers:"
wc -l < "$tmpdir/common"

# Filter each original list
for list in "${lists[@]}"; do
    outfile="${list%.lst}.common.lst"

    awk '
        NR==FNR {
            common[$1] = 1
            next
        }

        match($0, /qcdsf\.[0-9]+\.[0-9]+/) {
            id = substr($0, RSTART + 6, RLENGTH - 6)
            if (id in common)
                print
        }
    ' "$tmpdir/common" "$list" > "$outfile"

    echo "$list -> $outfile"
done
