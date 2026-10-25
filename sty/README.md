# Extracted runtime modules

Run `texlua scripts/unpack.lua` from the parent directory to create this directory
if needed and extract all 22 runtime modules. Alternatively, retain this file
and run `tex gradbars.ins` from the parent directory to extract all 22 runtime
`.sty` files into this directory. Install the complete set together in
`TEXMFHOME/tex/latex/gradbars/`, or copy it beside your main `.tex` file.

Keep this directory in source distributions: plain TeX cannot create missing
directories. No shell escape is required. The source archive contains this
README only; extraction creates the runtime files.
