-- gradbars: l3build semantic regressions and existing reproducible builders.
module = "gradbars"
sourcefiledir = "."
docfiledir = "docs"
sourcefiles = {"gradbars.dtx", "gradbars.ins"}
installfiles = {"gradbars*.sty", "tblrlibgradbars.sty"}
unpackfiles = {"gradbars.ins"}
testfiledir = "tests/l3build"
builddir = "build/l3build"
checkengines = {"pdftex", "xetex", "luatex"}
stdengine = "pdftex"
checkruns = 2
checkopts = "-interaction=nonstopmode -halt-on-error"
checksearch = true -- Keep TeX's external PGF/TikZ dependencies available.
specialformats = specialformats or {}
specialformats.latex = specialformats.latex or {}
specialformats.latex.luatex = {
  binary = "luahbtex", format = "lualatex", options = "-progname=lualatex"
}
function checkinit_hook()
  dofile("scripts/release.lua").runtime(unpackdir)
  local cache = builddir .. "/tex-cache"
  -- Windows CRT child environments cannot reliably pass non-ASCII cache paths.
  if os.type == "windows" then
    cache = (os.getenv("TEMP") or os.getenv("TMP")) .. "/gradbars-l3build-cache"
  end
  mkdir(cache)
  if os.setenv then
    os.setenv("TEXMFVAR", abspath(cache))
    os.setenv("TEXMFCACHE", abspath(cache))
  end
  return 0
end

-- TeX Live's Windows run() shells out to cd with an unconverted UTF-8 path.
-- Change directory through LuaFileSystem instead so non-ASCII projects work.
if os.type == "windows" then
  function run(dir, command)
    local previous = lfs.currentdir()
    local path = dir:gsub('^"', ''):gsub('"$', '')
    local ok, err = lfs.chdir(path)
    if not ok then error(err) end
    if options.debug then
      print(command)
      print("Lua font cache: " .. tostring(os.getenv("TEXMFCACHE")))
      command = command:gsub(" > nul", "")
    end
    local status, _, code = os.execute(command)
    assert(lfs.chdir(previous))
    if type(status) == "number" then return status end
    return status and 0 or (code or 1)
  end
end

-- Native l3build targets; design reference: OsbertWang/install-latex-guide-zh-cn.
-- This project-specific implementation remains MIT licensed.
local release = dofile("scripts/release.lua")
-- GitHub tracks sty/ only; CTAN carries the generated documented sources.
if fileexists("sty/gradbars.sty") then
  assert(run(".", "texlua scripts/source.lua") == 0, "Cannot generate CTAN sources")
else
  assert(fileexists("gradbars.dtx") and fileexists("gradbars.ins"), "Missing CTAN source files")
end
local version, releasedate = release.metadata()
ctanzip = "gradbars-ctan"
packtdszip = false
textfiles = {"LICENSE", "CHANGELOG.md"}
excludefiles = {"*~", "*.py", "*.pyc", "*.aux", "*.log"}
flattentds = false
typesetexe = "latexmk"
typesetopts = "-interaction=nonstopmode -halt-on-error -file-line-error -quiet"
typesetfiles = {"gradbars-manual.tex", "gradbars-manual-en.tex", "gradbars.dtx"}
typesetruns = 1
docfiles = {}
for _, path in ipairs(release.walk("docs")) do
  if release.allowed(path) then docfiles[#docfiles+1] = path:sub(6) end
end
docfiles[#docfiles+1] = "layouts/*.pdf"

local function makepdf(file, dir, engine, outdir)
  local cmd = typesetexe .. " " .. engine .. " " .. typesetopts
  if outdir then cmd = cmd .. ' -outdir="' .. outdir .. '"' end
  return runcmd(cmd .. ' "' .. file .. '"', dir, {"TEXINPUTS", "LUAINPUTS"})
end
function tex(file, dir, cmd)
  return runcmd((cmd or typesetexe .. " " .. typesetopts) .. ' "' .. file .. '"',
    dir or ".", {"TEXINPUTS", "LUAINPUTS"})
end
-- Let latexmk handle convergence, bibliography and index reruns itself.
function typeset(file, dir)
  local engine = file == "gradbars-manual.tex" and "-xelatex" or "-pdf"
  local status = makepdf(file, dir, engine)
  if status ~= 0 then return status end
  local stem = file:gsub("%.[^.]+$", "")
  release.logcheck(dir .. "/" .. stem .. ".log")
  local output = stem == "gradbars" and "gradbars-source" or stem
  release.copy(dir .. "/" .. stem .. ".pdf", output .. "-v" .. version .. ".pdf")
  release.copy(dir .. "/" .. stem .. ".pdf", "build/release/" .. output .. "-v" .. version .. ".pdf")
  return 0
end
function docinit_hook()
  release.runtime(unpackdir)
  for _, path in ipairs(release.walk("docs")) do
    if release.allowed(path) then release.copy(path, typesetdir .. "/" .. path) end
  end
  -- Source guide input and docs/ inputs resolve from the staged project root.
  for _, lang in ipairs({"en", "zh-cn"}) do
    mkdir(typesetdir .. "/Chapter/" .. lang)
    mkdir(typesetdir .. "/docs/Chapter/" .. lang)
  end
  for _, name in ipairs({"twocolumn", "longtable", "grayscale", "slides"}) do
    local dir = "docs/layouts"
    local status = makepdf(dir .. "/" .. name .. ".tex", typesetdir, "-xelatex", dir)
    if status ~= 0 then return status end
    release.logcheck(typesetdir .. "/" .. dir .. "/" .. name .. ".log")
    release.copy(typesetdir .. "/" .. dir .. "/" .. name .. ".pdf", dir .. "/" .. name .. ".pdf")
  end
  return 0
end
function copyctan()
  local target = ctandir .. "/" .. ctanpkg
  for _, name in ipairs({"LICENSE", "CHANGELOG.md", "gradbars.dtx", "gradbars.ins", "build.lua"}) do
    release.copy(name, target .. "/" .. name)
  end
  if fileexists("README.en.md") then
    release.write(target .. "/README.md", release.ctan_readme("README.en.md"))
  else
    release.copy("README.md", target .. "/README.md")
  end
  for _, dir in ipairs({"docs", "tests", "scripts"}) do
    for _, path in ipairs(release.walk(dir)) do
      if release.allowed(path) then release.copy(path, target .. "/" .. path) end
    end
  end
  for _, name in ipairs({"gradbars-manual", "gradbars-manual-en", "gradbars-source"}) do
    local file = name .. "-v" .. version .. ".pdf"
    release.copy(file, target .. "/" .. file)
  end
  for _, name in ipairs({"twocolumn", "longtable", "grayscale", "slides"}) do
    local file = "docs/layouts/" .. name .. ".pdf"
    release.copy(file, target .. "/" .. file)
  end
  return 0
end
uploadconfig = {
  pkg = module, version = version, author = "SuFan", uploader = "SuFan",
  email = os.getenv("CTAN_EMAIL"), license = "mit",
  summary = "Compact data graphics for LaTeX tables and inline text",
  description = "Bars, comparisons, sparklines, heat cells and distribution summaries with shared scales and native table interfaces.",
  ctanPath = "/graphics/pgf/contrib/gradbars/",
  repository = "https://github.com/Tape5try/gradbars",
  home = "https://github.com/Tape5try/gradbars",
  bugtracker = "https://github.com/Tape5try/gradbars/issues",
  announcement = os.getenv("CTAN_ANNOUNCEMENT") or "",
  note = os.getenv("CTAN_NOTE") or ""
}
-- Explicitly enabled only in the CTAN submission job; never auto-upload in doc/ctan.
ctanupload = os.getenv("GRADBARS_CTAN_UPLOAD") == "1"
