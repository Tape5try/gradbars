-- gradbars: l3build semantic regressions and existing reproducible builders.
module = "gradbars"
sourcefiledir = "sty"
sourcefiles = {"gradbars*.sty", "tblrlibgradbars.sty"}
installfiles = {"gradbars*.sty", "tblrlibgradbars.sty"}
unpackfiles = {}
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

-- Preserve the documented manual and CTAN directory/naming rules.
local python = os.getenv("GRADBARS_PYTHON") or "python"
target_list.doc.func = function()
  return run(".", '"' .. python .. '" scripts/build_manual.py')
end
target_list.ctan.func = function()
  return run(".", '"' .. python .. '" scripts/build_release.py')
end
