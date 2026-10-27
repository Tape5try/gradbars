-- MIT: independent starter verification with texlua and TeX Live, no Python.
local lfs=require('lfs')
local function read(p) local f=assert(io.open(p,'rb'));local s=f:read('*a');f:close();return s end
local function write(p,s) local f=assert(io.open(p,'wb'));f:write(s);f:close() end
local original=lfs.currentdir()
local here=arg[0]:match('^(.*)[/\\]') or '.'
assert(lfs.chdir(here));here=lfs.currentdir();assert(lfs.chdir(original))
local root=nil
if arg[1]=='--gradbars-root' then
  assert(arg[2],'Missing checkout path');assert(lfs.chdir(arg[2]));root=lfs.currentdir();assert(lfs.chdir(original))
  assert(lfs.attributes(root..'/sty/gradbars.sty'),'Development root must contain sty/gradbars.sty')
elseif arg[1] then error('Usage: texlua check-starter.lua [--gradbars-root CHECKOUT]') end
local work=os.tmpname();os.remove(work);assert(lfs.mkdir(work))
local sep=os.type=='windows' and ';' or ':'
assert(os.setenv, 'This checker requires the TeX Live texlua runtime')
local old=os.getenv('TEXINPUTS') or ''
os.setenv('TEXINPUTS',(root and root..'/sty'..sep or '')..here..sep..old..sep)
os.setenv('max_print_line','1000')
assert(lfs.chdir(work))
write('example.tex',read(here..'/example.tex'))
local function execute(cmd)
  local ok,_,code=os.execute(cmd);return type(ok)=='number' and ok or (ok and 0 or code or 1)
end
for _,engine in ipairs({'pdflatex','xelatex','lualatex'}) do
  assert(execute(engine..' -interaction=nonstopmode -halt-on-error -jobname=starter example.tex > run.stdout 2>&1')==0,
    engine..' failed; inspect '..work)
  local log=read('starter.log')
  assert(log:find('STARTER-CHECK:OK',1,true), 'Missing success marker')
  assert(not log:find('Overfull',1,true), 'Overfull starter example')
  assert(#read('starter.pdf')>0,'Missing PDF')
  write('negative.tex',read('example.tex'):gsub('\\begin{document}','\\gradbarsrequireversion{999.0.0}\n\\begin{document}',1))
  assert(execute(engine..' -interaction=nonstopmode -halt-on-error negative.tex > negative.stdout 2>&1')~=0,'Missing version rejection')
  assert(read('negative.stdout'):find('requires gradbars',1,true),'Wrong version diagnostic')
  print(engine..': independent starter and version guard passed.')
end
assert(lfs.chdir(original));os.setenv('TEXINPUTS',old)
-- Leave diagnostic output in the reported temporary directory for inspection.
print('Starter diagnostics: '..work)
