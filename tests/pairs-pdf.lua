-- MIT: verify pair delegation, raw alternatives and table structure after static cases.
local r=dofile('scripts/release.lua')
local pdf=dofile('scripts/pdf-structure.lua')
local engines=#arg>0 and arg or {'pdflatex','xelatex','lualatex'}
for _,engine in ipairs(engines) do
 local path='build/native-check/'..engine..'/v123-pair-tagged'
 local snapshot=pdf.snapshot(path..'.pdf')
 r.write(path..'.structure.txt',snapshot)
 local roles,alts={},{}
 for line in snapshot:gmatch('[^\n]+') do
  local role=line:match('^([^|]+)|');roles[role]=(roles[role] or 0)+1
  if role=='Figure' then
   local hex=assert(line:match('^Figure|[fF][eE][fF][fF]([%x]+)|'))
   alts[#alts+1]=hex:gsub('....',function(c)
    local n=tonumber(c,16);return n<128 and string.char(n) or '?' end)
  end
 end
 assert(roles.Table==2 and roles.TR==6 and roles.TH==4 and roles.TD==8,
  engine..': pair proxies changed native/host table structure')
 assert(#alts==8,engine..': expected eight Figures without trial/artifact duplicates')
 local fragments={
  ['Reference: 20.125. Current: 72.875. Change: 52.75.']=1,
  ['Reference: missing. Current: 0. Change: missing.']=3,
  ['Reference: 66. Current: 82. Change: 16.']=2,
  ['Interval: missing.']=1,['Outer paired panel.']=1}
 for fragment,expected in pairs(fragments) do
  local count=0
  for _,alt in ipairs(alts) do if alt:find(fragment,1,true) then count=count+1 end end
  assert(count==expected,engine..': unexpected alternative count for '..fragment)
 end
 print(engine..': eight pair Figures; two tables; raw, missing, zero and embedded alternatives preserved.')
end
