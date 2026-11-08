-- MIT: verify command-wrapper Figure count and raw alternatives after static cases.
local r=dofile('scripts/release.lua')
local pdf=dofile('scripts/pdf-structure.lua')
local engines=#arg>0 and arg or {'pdflatex','xelatex','lualatex'}
for _,engine in ipairs(engines) do
 local path='build/native-check/'..engine..'/v123-command-tagged'
 local snapshot=pdf.snapshot(path..'.pdf')
 r.write(path..'.structure.txt',snapshot)
 local roles={}
 for line in snapshot:gmatch('[^\n]+') do
  local role=line:match('^([^|]+)|');roles[role]=(roles[role] or 0)+1
 end
 assert(roles.Table==1 and roles.TR==5 and roles.TH==6 and roles.TD==4,
  engine..': declared cells changed the single-table/header/data structure')
 local alts={}
 for line in snapshot:gmatch('[^\n]+') do
  if line:match('^Figure|') then
   local hex=assert(line:match('^Figure|[fF][eE][fF][fF]([A-Fa-f0-9]+)|'))
   alts[#alts+1]=hex:gsub('....',function(c)
    local n=tonumber(c,16);return n<128 and string.char(n) or '?' end)
  end
 end
 assert(#alts==5,engine..': expected five actual Figures, no trial/blank duplicates')
 for _,fragment in ipairs({'Declared standalone bar.','Positioned heat cell.','Value: 0.6.','Value: 0.','Missing'}) do
  local found=false
  for _,alt in ipairs(alts) do if alt:lower():find(fragment:lower(),1,true) then found=true end end
  assert(found,engine..': missing alternative fragment '..fragment)
 end
 print(engine..': five command/Heat Figures; table trial and blank emit none; zero, missing and raw values preserved.')
end
