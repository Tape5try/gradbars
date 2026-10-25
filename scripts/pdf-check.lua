-- MIT: verify actual Figure alternatives and tagged table structures, using pdfe.
local r=dofile('scripts/release.lua')
local pdf=dofile('scripts/pdf-structure.lua')
local expected=dofile('tests/cases/pdf-expected.lua')
local lfs=require('lfs')
local runtime=lfs.attributes('sty/gradbars.sty') and 'sty' or 'build/l3build/unpacked'
for _,path in ipairs(r.walk(runtime)) do
 if path:match('%.sty$') then r.copy(path,'build/pdf-check/runtime/'..path:match('[^/]+$')) end
end
for _,engine in ipairs({'pdflatex','xelatex','lualatex'}) do
 local names={};for name in pairs(expected[engine]) do names[#names+1]=name end;table.sort(names)
 for _,name in ipairs(names) do
  local out='build/pdf-check/'..engine;r.write(out..'/.keep','')
  r.copy('tests/cases/'..name..'.tex','build/tests/'..name..'.tex')
  for pass=1,2 do
   local cmd='max_print_line=1000 TEXINPUTS="build/pdf-check/runtime:docs/libraries/starter:build/tests:" '..engine
    ..' -interaction=nonstopmode -halt-on-error -output-directory='..out..' build/tests/'..name..'.tex > '..out..'/'..name..'.stdout 2>&1'
   local ok,_,code=os.execute(cmd);assert(ok==true or ok==0,'PDF fixture failed: '..engine..'/'..name..' ('..tostring(code)..')')
  end
  local actual=pdf.snapshot(out..'/'..name..'.pdf')
  r.write(out..'/'..name..'.structure.txt',actual)
  assert(actual==expected[engine][name],'PDF semantics changed: '..engine..'/'..name..'; inspect '..out)
 end
 print(engine..': '..#names..' PDF structure fixtures passed; Figure alternatives and table spans/scopes match.')
 io.stdout:flush()
end
