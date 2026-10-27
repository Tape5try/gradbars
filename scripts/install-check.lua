-- MIT: extract and install the actual source ZIP in a clean directory.
local r = dofile('scripts/release.lua')
local lfs = require('lfs')
r.verify('gradbars-ctan.zip')
local target = 'build/isolated-source'
r.clean(target)
local z = assert(zip.open('gradbars-ctan.zip'))
for info in z:files() do
  if info.filename:sub(-1)~='/' then
    local f=assert(z:open(info.filename));r.write(target..'/'..info.filename,f:read('*a'));f:close()
  end
end
z:close()
local previous=lfs.currentdir(); assert(lfs.chdir(target..'/gradbars'))
local function execute(cmd)
  local ok,_,code=os.execute(cmd)
  assert(ok==true or ok==0, 'Isolated installation command failed: '..cmd..' ('..tostring(code)..')')
end
local function fails(cmd, output, diagnostic)
  local ok,_,code=os.execute(cmd..' > '..output..' 2>&1')
  assert(ok~=true and ok~=0, 'Expected installation failure: '..cmd)
  assert(r.read(output):gsub('%s+',' '):find(diagnostic,1,true),
    'Wrong installation diagnostic: '..output..' ('..tostring(code)..')')
end
local function modules(dir)
  for name in lfs.dir('.') do
    assert(not name:match('%.sty$'), 'Unexpected root runtime module: '..name)
  end
  local n=0
  for name in lfs.dir(dir) do if name:match('%.sty$') then n=n+1 end end
  assert(n==22,'Expected all 22 extracted runtime modules in '..dir)
end
local function remove_sty()
  if not lfs.attributes('sty') then return end
  for name in lfs.dir('sty') do
    if name~='.' and name~='..' then assert(os.remove('sty/'..name)) end
  end
  assert(lfs.rmdir('sty'))
end
if lfs.attributes('sty/README.md','mode')=='file' then
  execute('tex -interaction=nonstopmode -halt-on-error gradbars.ins > extraction.stdout 2>&1')
else
  fails('tex -interaction=nonstopmode -halt-on-error gradbars.ins','missing-marker.stdout','Run texlua scripts/unpack.lua')
  execute('texlua scripts/unpack.lua > extraction.stdout 2>&1')
end
modules('sty')
-- An existing directory without its marker also needs the Lua repair path.
assert(os.remove('sty/README.md'))
fails('tex -interaction=nonstopmode -halt-on-error gradbars.ins','missing-marker.stdout','Run texlua scripts/unpack.lua')
execute('texlua scripts/unpack.lua > marker-repair.stdout 2>&1')
modules('sty')
-- CTAN may remove the otherwise empty directory before distribution.
remove_sty()
fails('tex -interaction=nonstopmode -halt-on-error gradbars.ins','missing-directory.stdout','Run texlua scripts/unpack.lua')
execute('texlua scripts/unpack.lua > auto-extraction.stdout 2>&1')
modules('sty')
remove_sty()
execute('l3build unpack > native-unpack.stdout 2>&1')
modules('build/l3build/unpacked/sty')
if lfs.attributes('tests/l3build', 'mode')=='directory' then
  execute('l3build check > native-check.stdout 2>&1')
else
  fails('l3build check','native-check.stdout','Development tests are absent')
end
execute('texlua scripts/unpack.lua > installed-runtime.stdout 2>&1')
modules('sty')
for _,engine in ipairs({'pdflatex','xelatex','lualatex'}) do
  execute('max_print_line=1000 TEXINPUTS="./sty//:.:docs/libraries/starter:" '..engine..' -interaction=nonstopmode -halt-on-error -jobname=isolated-'..engine..' docs/examples/domain-reports.tex > '..engine..'.stdout 2>&1')
  r.logcheck('isolated-'..engine..'.log')
  local log=r.read('isolated-'..engine..'.log')
  assert(log:find('(./sty/gradbars.sty',1,true),'Installed elsewhere: '..engine)
  print(engine..': isolated CTAN source extraction and domain reports passed.')
end
assert(lfs.chdir(previous))
