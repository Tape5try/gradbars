-- MIT: verify actual longtable shipout pages, not token-level keep hints.
local r=dofile('scripts/release.lua')
local engines=#arg>0 and arg or {'pdflatex','xelatex','lualatex'}
for _,engine in ipairs(engines) do
 for _,name in ipairs({'v140-long','v140-long-grid','v140-long-rows','v140-long-none','v121-long'}) do
 local aux=r.read('build/native-check/'..engine..'/'..name..'.aux')
 local pages,counts={},{}
 for key,page in aux:gmatch('\\newlabel{([^}]+)}{{[^}]*}{([^}]+)}') do
  pages[key]=assert(tonumber(page),'Non-numeric page');counts[key]=(counts[key] or 0)+1
 end
 local headings,summaries,rows=0,0,0
 for key in pairs(pages) do
  if key:match('^heading%-') then headings=headings+1 end
  if key:match('^summary%-') then summaries=summaries+1 end
  if key:match('^row%-') then rows=rows+1 end
 end
 assert(headings==12 and summaries==12 and rows==72,engine..': unexpected hierarchy output count')
 local function page(key)
  assert(pages[key],engine..': missing shipout label '..key)
  assert(counts[key]==1,engine..': duplicate output label '..key)
  return pages[key]
 end
 for parent=1,3 do
  local parentNode=(parent-1)*4+1
  local first=(parent-1)*24+1
  assert(page('heading-'..parentNode)==page('row-'..first),engine..': orphan parent heading')
  for leaf=1,3 do
   local node=parentNode+leaf
   local start=first+(leaf-1)*8
   assert(page('heading-'..node)==page('row-'..start),engine..': orphan leaf heading')
   assert(page('summary-'..node)==page('row-'..(start+7)),engine..': separated leaf summary')
  end
  assert(page('summary-'..parentNode)==page('row-'..(parent*24)),engine..': separated parent summary')
 end
 assert(page('overall-summary')==page('row-72'),engine..': separated overall summary')
 assert(page('row-72')>page('row-1'),engine..': pagination fixture did not cross pages')
 print(engine..'/'..name..': headings and 12 summaries remain attached on actual pages.')
 end
end
