-- MIT: replay static TeX regressions under all supported engines using texlua.
local lfs = require('lfs')
local r = dofile('scripts/release.lua')
local engines = #arg > 0 and arg or {'pdflatex','xelatex','lualatex'}
local cases = dofile('tests/cases/manifest.lua')
local snapshot='build/native-check/runtime-'..table.concat(engines,'-')
local runtime = lfs.attributes('sty/gradbars.sty') and 'sty' or 'build/l3build/unpacked'
assert(lfs.attributes(runtime .. '/gradbars.sty'), 'Run l3build unpack first')
for _, path in ipairs(r.walk(runtime)) do
  if path:match('%.sty$') then r.copy(path, snapshot..'/'..path:match('[^/]+$')) end
end
local function execute(command)
  local status, _, code = os.execute(command)
  return type(status)=='number' and status or (status and 0 or (code or 1))
end
local function count(s, needle)
  local n,p=0,1
  while true do local a,b=s:find(needle,p,true); if not a then return n end;n=n+1;p=b+1 end
end
for _, path in ipairs(r.walk('tests/cases')) do
  if path:match('%.tex$') or path:match('%.csv$') or path:match('%.sty$') then
    r.copy(path,'build/tests/'..path:match('[^/]+$'))
  end
end
for _, engine in ipairs(engines) do
  assert(engine=='pdflatex' or engine=='xelatex' or engine=='lualatex','Unsupported engine')
  local out='build/native-check/'..engine
  r.write(out..'/.keep','')
  local selected={}
  for _,case in ipairs(cases) do if not case.engines or case.engines[engine] then selected[#selected+1]=case end end
  for i, case in ipairs(selected) do
    local source=case.sources and case.sources[engine] or case.source or (case.name..'.tex')
    local cmd='max_print_line=1000 TEXINPUTS="'..snapshot..':docs/libraries/starter:build/tests:" '..engine
      ..' -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="'..out
      ..'" -jobname='..case.name..' "build/tests/'..source..'" > "'..out..'/'..case.name..'.stdout" 2>&1'
    -- The runner is used in Linux CI; native l3build check remains cross-platform.
    local result
    for pass=1,(case.passes or 1) do result=execute(cmd);if result~=0 then break end end
    local log=r.read(out..'/'..case.name..'.stdout')
    local diagnostic=case.errors and case.errors[engine] or case.error
    if diagnostic then
      assert(result~=0,engine..'/'..case.name..': expected failure')
      -- file-line-error prefixes replace the leading "!", but preserve diagnostics.
      assert(log:gsub('%s+',' '):find(diagnostic:gsub('%s+',' '),1,true),engine..'/'..case.name..': wrong diagnostic')
    else
      assert(result==0,engine..'/'..case.name..': compilation failed; see '..out)
      assert(count(log,'Overfull')<=case.overfull,engine..'/'..case.name..': new overfull box')
      assert(count(log,'Package gradbars Warning')<=case.warnings,engine..'/'..case.name..': new warning')
    end
    if i%25==0 or i==#selected then print(engine..': '..i..'/'..#selected..' cases passed');io.stdout:flush() end
  end
end
print('Static regression suite passed without Python.')
