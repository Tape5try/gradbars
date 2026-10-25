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
execute('tex -interaction=nonstopmode -halt-on-error gradbars.ins > extraction.stdout 2>&1')
execute('l3build check > native-check.stdout 2>&1')
local n=0
for name in lfs.dir('.') do if name:match('%.sty$') then n=n+1 end end
assert(n==22,'Expected all 22 extracted runtime modules')
for _,engine in ipairs({'pdflatex','xelatex','lualatex'}) do
  execute('max_print_line=1000 TEXINPUTS=".:docs/libraries/starter:" '..engine..' -interaction=nonstopmode -halt-on-error -jobname=isolated-'..engine..' docs/examples/domain-reports.tex > '..engine..'.stdout 2>&1')
  r.logcheck('isolated-'..engine..'.log')
  local log=r.read('isolated-'..engine..'.log')
  assert(log:find('(./gradbars.sty',1,true),'Installed elsewhere: '..engine)
  print(engine..': isolated CTAN source extraction and domain reports passed.')
end
assert(lfs.chdir(previous))
