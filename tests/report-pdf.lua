-- MIT: assertions on actual Figure structure, not only successful compilation.
local r=dofile('scripts/release.lua')
local pdf=dofile('scripts/pdf-structure.lua')
local engines=#arg>0 and arg or {'pdflatex','xelatex','lualatex'}
local function alternatives(path)
 local s=pdf.snapshot(path);local out={}
 for line in s:gmatch('[^\n]+') do
  if line:match('^Figure|') then
   local hex=assert(line:match('^Figure|[fF][eE][fF][fF]([A-Fa-f0-9]+)|'),'Missing alternative')
   out[#out+1]=hex:gsub('....',function(c)local n=tonumber(c,16);return n<128 and string.char(n) or '?' end)
  end
 end
 return out,s
end
for _,engine in ipairs(engines) do
 local root='build/native-check/'..engine..'/'
 local alts,s=alternatives(root..'v121-tagged.pdf')
 r.write(root..'v121-tagged.structure.txt',s)
 assert(#alts==6,engine..': expected six visible standalone/outer Figures')
 local required={'Current-value bar: final position: 80',
  'Current-value bar: final position: missing', 'Raw sample rug',
  'Explicit metric card.', 'Embedded report card.'}
 for _,fragment in ipairs(required) do
  local found=false;for _,a in ipairs(alts) do if a:find(fragment,1,true) then found=true end end
  assert(found,engine..': missing '..fragment)
 end
 local combined=table.concat(alts,'\n')
 assert(combined:find('observation 1: 0; observation 2: 40; observation 3: missing; observation 4: 80.',1,true),'Full history or zero lost')
 assert(combined:find('Report metric: Review score;',1,true),'Metric metadata lost')
 assert(combined:find('0, 2, 2, 4.',1,true),'Rug duplicates lost')
 assert(combined:find('n=4; missing=1;',1,true),'Rug sample count changed')
 local native=alternatives(root..'v121-table-tagged.pdf')
 assert(#native==6,engine..': expected six data-cell Figures without measurement duplicates')
 local adapters=alternatives(root..'v121-adapter-tagged.pdf')
 assert(#adapters==4,'Adapter measurement duplicated Figures')
 local pgf=alternatives(root..'v121-pgf-tagged.pdf')
 assert(#pgf==4,'PGF headers or number cells emitted a Figure')
 local pgftext=table.concat(pgf,'\n')
 assert(pgftext:find('70',1,true) and pgftext:find('Value: 0',1,true),'PGF raw body values lost')
 print(engine..': report cards/rugs have exact Figure counts, full history, final NA, zero, duplicate samples and explicit alternatives.')
end
