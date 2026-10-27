-- MIT: native l3build helpers for gradbars; no external language runtime.
local lfs = require('lfs')
local M = {}
M.license_note = 'The gradbars package and original documentation are MIT licensed. '
  .. 'Only the attributed table data adapted in docs/examples/precision-recall.tex '
  .. '(Sebastiano, https://tex.stackexchange.com/a/767118) are CC BY-SA 4.0; '
  .. 'the example records the adaptation and attribution.'
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
function M.copy(src, dest)
  M.write(dest, M.read(src))
  local attr = assert(lfs.attributes(src))
  assert(lfs.touch(dest, attr.access, attr.modification), 'Cannot preserve timestamp: '..dest)
end
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
  if path:match('/ctan%-upload%.md$') or path:match('^docs/releases/') then return false end
  return path:match('%.tex$') or path:match('%.md$') or path:match('%.csv$')
    or path:match('%.sty$') or path:match('%.svg$') or path:match('%.png$')
    or path:match('%.jpg$') or path:match('%.bib$') or path:match('%.lua$')
    or path:match('%.lvt$') or path:match('%.tlg$')
end
-- CTAN text/source files are data, including Lua scripts invoked through texlua.
function M.permissions(dir)
  if os.type == 'windows' then return end
  local quoted = "'" .. dir:gsub("'", "'\\''") .. "'"
  for _, spec in ipairs({'f -exec chmod 644 {} +', 'd -exec chmod 755 {} +'}) do
    local ok = os.execute('find '..quoted..' -type '..spec)
    assert(ok == true or ok == 0, 'Cannot normalize CTAN permissions')
  end
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
    .. description .. '\nAuthor and maintainer: SuFan (Tape5try).\n'
    .. M.license_note .. ' See LICENSE for the MIT terms.\n'
    .. 'Repository and issues: https://github.com/Tape5try/gradbars\n\n'
    .. [[## Installation from the CTAN source archive

Generated runtime modules are not repeated in this source archive. To create
sty/ automatically and extract the modules, run from this directory:

```sh
texlua scripts/unpack.lua
```

Alternatively, if sty/README.md is present, run:

```sh
tex gradbars.ins
```

The sty/ directory receives all 22 extracted .sty files. Plain TeX does not create
directories; use the Lua entry above if sty/ or its README marker is missing.
No runtime .sty files are written into the source root.

Install all 22 extracted .sty files from sty/ together in TEXMFHOME/tex/latex/gradbars/,
or place the complete set alongside your document. Refresh the filename database
if required by your distribution. Do not install only gradbars.sty.

## Dependencies and documentation

]] .. dependencies .. [[

Current Chinese, English and source-guide PDFs are supplied in this directory.
Complete documentation sources, data and example libraries are under docs/.
The Chinese manual requires XeLaTeX and ctex/Fandol; the English manual and
source guide use pdfLaTeX. No Python interpreter is required.

## Rebuild documentation

```sh
l3build unpack
l3build doc
```

l3build extracts and stages the runtime automatically. texlua and latexmk are
provided by TeX Live. scripts/source.lua is only needed in the development
checkout containing sty/; this source archive already contains gradbars.dtx/ins.
The complete regression suite and tests/ are maintained in the GitHub checkout.
Run l3build check, scripts/check.lua and scripts/pdf-check.lua there. A CTAN
source package that omits development tests cannot run the regression suite;
l3build check reports this explicitly instead of claiming an empty test pass.
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
local function archive_path(name)
  assert(name:sub(1,9)=='gradbars/' and not name:find('[^A-Za-z0-9_./%-]')
    and not name:find('//',1,true), 'Unsafe archive path: '..name)
  for part in name:gmatch('[^/]+') do
    assert(part:sub(1,1)~='.', 'Unsafe archive path: '..name)
  end
  local lower=name:lower()
  assert(not lower:match('^gradbars/tests/') and not lower:match('^gradbars/build/')
    and not lower:match('^gradbars/docs/releases/'), 'Development file in archive: '..name)
  local base = lower:match('[^/]+$') or ''
  assert(not ({['roadmap.md']=true,['upload-restrictions.md']=true,
    ['readme.ctan.md']=true,['resubmission-notes.txt']=true,['ctan-upload.md']=true})[base],
    'Local maintenance file in archive: '..name)
  assert(not lower:match('%.py[c]?$') and not lower:find('__pycache__',1,true), 'Python in archive: '..name)
  local ext = lower:match('%.([^./]+)$')
  assert(not ({aux=true,log=true,toc=true,out=true,fls=true,fdb_latexmk=true,
    idx=true,ilg=true,ind=true,lof=true,lot=true,bbl=true,blg=true,xdv=true,
    zip=true,bak=true,tmp=true})[ext] and not lower:match('%.synctex%.gz$'),
    'Temporary file in archive: '..name)
  assert((not lower:match('^gradbars/sty/') or name=='gradbars/sty/' or name=='gradbars/sty/README.md')
    and not lower:match('^gradbars/gradbars[^/]*%.sty$') and lower~='gradbars/tblrlibgradbars.sty',
    'Generated file in source archive: '..name)
end
function M.verify(archive)
  -- luazip omits Unix mode bits; read them from the ZIP central directory.
  local raw = M.read(archive)
  local ending
  for p = #raw-21, math.max(1,#raw-65557), -1 do
    if raw:sub(p,p+3) == 'PK\005\006' and p+21+string.unpack('<I2',raw,p+20)==#raw then ending=p;break end
  end
  assert(ending, 'Missing ZIP central directory')
  local disk, startdisk, diskentries, entries, size, offset = string.unpack('<I2I2I2I2I4I4',raw,ending+4)
  assert(disk==0 and startdisk==0 and diskentries==entries and entries~=65535,
    'Unsupported split or ZIP64 archive')
  local cursor = offset+1
  assert(cursor+size==ending, 'Invalid ZIP central directory bounds')
  local paths, folded, unix = {}, {}, 0
  for _ = 1,entries do
    assert(raw:sub(cursor,cursor+3)=='PK\001\002','Invalid ZIP directory entry')
    local made = string.unpack('<I2',raw,cursor+4)
    local dostime,dosdate = string.unpack('<I2I2',raw,cursor+12)
    local n,e,c = string.unpack('<I2I2I2',raw,cursor+28)
    local attrs = string.unpack('<I4',raw,cursor+38)
    local localoffset = string.unpack('<I4',raw,cursor+42)+1
    local name = raw:sub(cursor+46,cursor+45+n)
    assert(cursor+46+n+e+c<=ending, 'Invalid ZIP directory bounds: '..name)
    archive_path(name)
    assert(not paths[name] and not folded[name:lower()], 'Duplicate archive path: '..name)
    paths[name]=true;folded[name:lower()]=true
    local year,month,day = (dosdate >> 9)+1980, (dosdate >> 5) & 15, dosdate & 31
    local days={31,year%4==0 and (year%100~=0 or year%400==0) and 29 or 28,31,30,31,30,31,31,30,31,30,31}
    assert(dosdate~=33 and days[month] and day>=1 and day<=days[month]
      and (dostime >> 11)<24 and ((dostime >> 5) & 63)<60 and (dostime & 31)<30,
      'Missing/default ZIP timestamp: '..name)
    assert(raw:sub(localoffset,localoffset+3)=='PK\003\004', 'Invalid ZIP local header: '..name)
    local localtime,localdate = string.unpack('<I2I2',raw,localoffset+10)
    local localnamesize = string.unpack('<I2',raw,localoffset+26)
    assert(raw:sub(localoffset+30,localoffset+29+localnamesize)==name
      and localtime==dostime and localdate==dosdate, 'Conflicting ZIP local header: '..name)
    if made//256 == 3 then
      local fullmode = attrs >> 16
      local kind,mode = fullmode & 61440, fullmode & 4095
      local expected = name:sub(-1)=='/' and 493 or 420 -- 0755 / 0644
      local expectedkind = name:sub(-1)=='/' and 16384 or 32768
      assert((kind==0 or kind==expectedkind) and mode==expected,
        'Bad archive permissions: '..name..' ('..string.format('%o',fullmode)..')')
      unix=unix+1
    end
    cursor=cursor+46+n+e+c
  end
  assert(cursor==ending, 'Incorrect ZIP central directory size')
  local z = assert(zip.open(archive), archive)
  local count = 0; local files,basenames,contents,bodies = {},{},{},{}
  for info in z:files() do
    local name = info.filename
    assert(paths[name], 'Unlisted archive path: '..name)
    if name:sub(-1)~='/' then
      local base = name:match('[^/]+$'):lower()
      if base~='readme.md' then
        assert(not basenames[base], 'Repeated filename: '..name..' and '..tostring(basenames[base]))
        basenames[base]=name
      end
      local f=assert(z:open(name));local body=f:read('*a');f:close()
      assert(not contents[body], 'Duplicate contents: '..name..' and '..tostring(contents[body]))
      contents[body]=name
      bodies[name]=body
    end
    assert(not files[name], 'Duplicate archive path: '..name); files[name]=true;count=count+1
  end
  assert(count==entries, 'ZIP entry count mismatch')
  for _, name in ipairs({'README.md','LICENSE','gradbars.dtx','gradbars.ins','build.lua','scripts/release.lua','scripts/unpack.lua',
    'docs/examples/precision-recall.tex'}) do
    assert(files['gradbars/'..name], 'Missing archive file: '..name)
  end
  local example=bodies['gradbars/docs/examples/precision-recall.tex']
  assert(example:find('CC BY-SA 4.0',1,true) and example:find('Sebastiano',1,true)
    and example:find('https://tex.stackexchange.com/a/767118',1,true), 'Missing adapted-example attribution')
  local v = M.metadata()
  for _, stem in ipairs({'gradbars-manual','gradbars-manual-en','gradbars-source'}) do
    assert(files['gradbars/'..stem..'-v'..v..'.pdf'] or files['gradbars/docs/'..stem..'.pdf'], 'Missing PDF: '..stem)
  end
  z:close(); print('Verified CTAN source archive: '..count..' entries; '..unix
    ..' Unix permissions checked; no Python or generated runtime modules.')
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
