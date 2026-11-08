-- MIT: independent semantic assertions on real tagged PDF output.
local r=dofile('scripts/release.lua')
local pdf=dofile('scripts/pdf-structure.lua')
local engines=#arg>0 and arg or {'pdflatex','xelatex','lualatex'}
for _,engine in ipairs(engines) do
 local path='build/native-check/'..engine..'/v1340-tagged.pdf'
 local snapshot=pdf.snapshot(path)
 r.write('build/native-check/'..engine..'/v1340-tagged.structure.txt',snapshot)
 local descriptions={}
 for line in snapshot:gmatch('[^\n]+') do
  assert(line:match('^Figure|'),'Unexpected structure in composition fixture: '..line)
  local hex=assert(line:match('^Figure|[fF][eE][fF][fF]([A-Fa-f0-9]+)|'),'Missing Figure alternative')
  local plain=hex:gsub('....',function(c) local n=tonumber(c,16);assert(n<128,'Expected ASCII fixture');return string.char(n) end)
  descriptions[#descriptions+1]=plain
 end
 assert(#descriptions==8,engine..': expected exactly one Figure per visible standalone/outer composition')
 local expected={
  'Fixed reference band (not observations or a confidence interval): 20 to 60.',
  'Endpoint panel: first position: 0; last position: 70; change: 70.',
  'Endpoint panel: first position: missing; last position: 70; change: missing',
  'Endpoint panel: first position: 10; last position: missing; change: missing',
  'Endpoint panel: first position: missing; last position: missing; change: missing',
  'Explicit endpoint trend.', 'Outer composition picture.'}
 for _,s in ipairs(expected) do
  local count=0
  for _,d in ipairs(descriptions) do if d:find(s,1,true) then count=count+1 end end
  assert(count==(s==expected[1] and 2 or 1),engine..': wrong alternative count for '..s)
 end
 local full=false
 for _,d in ipairs(descriptions) do
  if d:find('first position: 0;',1,true) then
   assert(d:find('observation 1: 0; observation 2: missing; observation 3: 70.',1,true),'Full series lost')
   assert(d:find('Vertical range: -10 to 100.',1,true),'Shared range lost')
   assert(d:find('share the same value range and unit.',1,true),'Panel contract lost')
   full=true
  end
 end
 assert(full,'Missing combined alternative')
 print(engine..': 8 Figures; series, fixed band, endpoint NA, explicit Alt and embedded/artifact/off semantics passed.')
 local native=pdf.snapshot('build/native-check/'..engine..'/v140-table-tagged.pdf')
 local figures=0
 for line in native:gmatch('[^\n]+') do if line:match('^Figure|') then figures=figures+1 end end
 assert(figures==2,engine..': native trend measurement duplicated or omitted Figures')
 print(engine..': native trend table has exactly 2 Figures for 2 data cells.')

end
