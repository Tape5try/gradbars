-- MIT: native l3build helpers for gradbars; no external language runtime.
local lfs = require('lfs')
local M = {}
function M.read(path)
  local f = assert(io.open(path, 'rb'), path); local s = f:read('*a'); f:close(); return s
end
function M.write(path, s)
  local dir = path:match('^(.*)/[^/]+$')
  if dir then
    local partial = ''
    for part in dir:gmatch('[^/]+') do
      partial = partial == '' and part or partial .. '/' .. part
      if not lfs.attributes(partial) then assert(lfs.mkdir(partial)) end
    end
  end
  local f = assert(io.open(path, 'wb')); f:write(s); f:close()
end
function M.copy(src, dest) M.write(dest, M.read(src)) end
function M.walk(dir)
  local paths = {}
  if not lfs.attributes(dir) then return paths end
  for name in lfs.dir(dir) do
    if name ~= '.' and name ~= '..' and name ~= '__pycache__' then
      local path = dir .. '/' .. name
      if lfs.symlinkattributes(path, 'mode') == 'directory' then
        for _, p in ipairs(M.walk(path)) do paths[#paths+1] = p end
      elseif lfs.symlinkattributes(path, 'mode') == 'file' then paths[#paths+1] = path end
    end
  end
  table.sort(paths); return paths
end
function M.allowed(path)
  if path:match('/ctan%-upload%.md$') then return false end
  return path:match('%.tex$') or path:match('%.md$') or path:match('%.csv$')
    or path:match('%.sty$') or path:match('%.svg$') or path:match('%.png$')
    or path:match('%.jpg$') or path:match('%.bib$') or path:match('%.lua$')
    or path:match('%.lvt$') or path:match('%.tlg$')
end
function M.runtime(dir)
  if not lfs.attributes('sty/gradbars.sty') then return end
  local count = 0
  for _, path in ipairs(M.walk('sty')) do
    if path:match('%.sty$') then
      local function normalize(s) return s:gsub('\r\n','\n'):gsub('[ \t]+\n','\n') end
      assert(normalize(M.read(path)) == normalize(M.read(dir .. '/' .. path:match('[^/]+$'))),
        'Docstrip mismatch: ' .. path .. '; run texlua scripts/source.lua')
      count = count+1
    end
  end
  assert(count == 22, 'Expected 22 runtime modules'); print('Docstrip round trip: 22 modules match.')
end
function M.clean(dir)
  assert(dir:match('^build/[%w/_-]+$'), 'Refuse to clean outside build/')
  local function remove(path)
    if lfs.symlinkattributes(path,'mode')=='directory' then
      for name in lfs.dir(path) do if name~='.' and name~='..' then remove(path..'/'..name) end end
      assert(lfs.rmdir(path))
    elseif lfs.symlinkattributes(path) then assert(os.remove(path)) end
  end
  remove(dir)
end
-- Derive the CTAN entry from the tracked English README; no local template required.
function M.ctan_readme(path)
  local english = M.read(path)
  local description = assert(english:match('(Built on PGF/TikZ.-)\n## Installation'), 'English README features section missing')
  local dependencies = assert(english:match('(Requires LaTeX [^\n]+)'), 'English README dependencies missing')
  local version, date = M.metadata()
  return '# gradbars\n\nVersion ' .. version .. ' (' .. date .. ').\n\n'
    .. description .. '\nAuthor and maintainer: SuFan (Tape5try). Licensed under MIT; see LICENSE.\n'
    .. 'Repository and issues: https://github.com/Tape5try/gradbars\n\n'
    .. [[## Installation from the CTAN source archive

Generated runtime modules are not repeated in this source archive. Run:

```sh
tex gradbars.ins
```

Install all 22 extracted .sty files together in TEXMFHOME/tex/latex/gradbars/,
or place the complete set alongside your document. Refresh the filename database
if required by your distribution. Do not install only gradbars.sty.

## Dependencies and documentation

]] .. dependencies .. [[

Current Chinese, English and source-guide PDFs are supplied in this directory.
Complete documentation sources, data and example libraries are under docs/.
The Chinese manual requires XeLaTeX and ctex/Fandol; the English manual and
source guide use pdfLaTeX. No Python interpreter is required.

## Rebuild and test

```sh
l3build check
l3build doc
texlua scripts/check.lua
texlua scripts/pdf-check.lua
```

l3build extracts and stages the runtime automatically. texlua and latexmk are
provided by TeX Live. scripts/source.lua is only needed in the development
checkout containing sty/; this source archive already contains gradbars.dtx/ins.
]]
end
function M.metadata()
  local s = M.read('gradbars.dtx')
  local date, version = s:match('\\ProvidesPackage{gradbars}%[([%d/]+) v([%d.]+)')
  assert(date and version, 'Missing package version/date')
  return version, date
end
function M.logcheck(path)
  local s = M.read(path)
  assert(not s:find('Overfull',1,true), 'Overfull box: ' .. path)
  assert(not s:lower():find('undefined references',1,true), 'Undefined references: ' .. path)
end
function M.verify(archive)
  local z = assert(zip.open(archive), archive)
  local count = 0; local files = {}
  for info in z:files() do
    local name = info.filename
    assert(name:sub(1,9) == 'gradbars/' and not name:find('..',1,true), 'Unsafe archive path: '..name)
    assert(not name:match('%.py[c]?$') and not name:find('__pycache__',1,true), 'Python in archive: '..name)
    assert(not name:match('^gradbars/sty/') and not name:match('%.aux$') and not name:match('%.log$'), 'Generated file in source archive: '..name)
    assert(not files[name], 'Duplicate archive path: '..name); files[name]=true;count=count+1
  end
  for _, name in ipairs({'README.md','LICENSE','gradbars.dtx','gradbars.ins','build.lua','scripts/release.lua'}) do
    assert(files['gradbars/'..name], 'Missing archive file: '..name)
  end
  local v = M.metadata()
  for _, name in ipairs({'gradbars-manual-v'..v..'.pdf','gradbars-manual-en-v'..v..'.pdf','gradbars-source-v'..v..'.pdf'}) do
    assert(files['gradbars/'..name], 'Missing PDF: '..name)
  end
  z:close(); print('Verified CTAN source archive: '..count..' entries; no Python or generated runtime modules.')
end
if arg and arg[0] and arg[0]:match('release%.lua$') then
  if arg[1]=='--verify' then
    M.verify('gradbars-ctan.zip')
  elseif arg[1]=='--tag' then
    local v,d=M.metadata()
    assert(arg[2]=='v'..v, 'Tag must match package version v'..v)
    local modules=0
    for name,date,ver in M.read('gradbars.dtx'):gmatch('\\ProvidesPackage{([^}]+)}%[([%d/]+) v([%d.]+)') do
      assert(date==d and ver==v, 'Module metadata mismatch: '..name);modules=modules+1
    end
    assert(modules==22,'Expected metadata for all 22 modules')
    assert(M.read('CHANGELOG.md'):find('## '..v..' — '..d:gsub('/','-'),1,true),'CHANGELOG release metadata mismatch')
    for _,file in ipairs({'README.md','README.en.md'}) do
      assert(M.read(file):find('**v'..v..' ·',1,true), 'README version mismatch: '..file)
    end
    assert(d<=os.date('!%Y/%m/%d'), 'Planned future date; finalize release metadata first')
    assert(not M.read('README.md'):find('尚未发布',1,true), 'Finalize development README before a stable release')
    print('Release tag and date verified: '..arg[2])
  else error('Usage: texlua scripts/release.lua --verify | --tag vVERSION') end
end
return M
