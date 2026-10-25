-- MIT: contrast samples and CVD design previews; numerical matrices from
-- Machado/Oliveira/Fernandes (2009), DOI 10.1109/TVCG.2009.113.
-- Simulations are supplementary design evidence, not certification.
local r=dofile('scripts/release.lua')
local hex={'0072B2','E69F00','009E73','CC79A7','56B4E9','D55E00','F0E442'}
local matrices={
 {'Protanopia',{{.152286,1.052583,-.204868},{.114503,.786281,.099216},{-.003882,-.048116,1.051998}}},
 {'Deuteranopia',{{.367322,.860646,-.227968},{.280085,.672501,.047413},{-.011820,.042940,.968881}}},
 {'Tritanopia',{{1.255528,-.076749,-.178779},{-.078411,.930809,.147602},{.004733,.691367,.303900}}}
}
local function linear(v) return v<=.04045 and v/12.92 or ((v+.055)/1.055)^2.4 end
local function encoded(v) v=math.max(0,math.min(1,v));return v<=.0031308 and 12.92*v or 1.055*v^(1/2.4)-.055 end
local function luminance(c) return linear(c[1])*.2126+linear(c[2])*.7152+linear(c[3])*.0722 end
local colors={}
for _,h in ipairs(hex) do colors[#colors+1]={tonumber(h:sub(1,2),16)/255,tonumber(h:sub(3,4),16)/255,tonumber(h:sub(5,6),16)/255} end
local previews={{'Original',colors},{'Grayscale',{}}}
for _,c in ipairs(colors) do local v=encoded(luminance(c));table.insert(previews[2][2],{v,v,v}) end
for _,m in ipairs(matrices) do
 local row={}
 for _,c in ipairs(colors) do
  local out={}
  for _,weights in ipairs(m[2]) do
   local v=0;for i=1,3 do v=v+weights[i]*linear(c[i]) end;out[#out+1]=encoded(v)
  end
  row[#row+1]=out
 end
 previews[#previews+1]={m[1],row}
end
local minima={}
for _,ramp in ipairs({{'sequential',{0,114/255,178/255}},{'diverging-low',{213/255,94/255,0}}}) do
 local low=math.huge
 for i=0,1000 do
  local c={};for j=1,3 do c[j]=1-i/1000+i/1000*ramp[2][j] end
  local lum=luminance(c);local ratio=lum>.179 and (lum+.05)/.05 or 1.05/(lum+.05)
  low=math.min(low,ratio)
 end
 assert(low>=4.5,'Insufficient contrast: '..ramp[1]);minima[#minima+1]=string.format('%q: %.12f',ramp[1],low)
end
r.write('build/accessible/contrast.json','{"black_white_auto_minimum":{'..table.concat(minima,',')..'},"samples_per_ramp":1001,"certification":false}\n')
local svg={'<svg xmlns="http://www.w3.org/2000/svg" width="920" height="420"><rect width="100%" height="100%" fill="white"/><g font-family="sans-serif" font-size="14"><text x="20" y="26">Color roles under design simulations</text>'}
for i,preview in ipairs(previews) do
 local y=60+(i-1)*62
 svg[#svg+1]=string.format('<text x="20" y="%d">%s</text>',y+20,preview[1])
 for j,c in ipairs(preview[2]) do
  local h=string.format('#%02x%02x%02x',math.floor(c[1]*255+.5),math.floor(c[2]*255+.5),math.floor(c[3]*255+.5))
  svg[#svg+1]=string.format('<rect x="%d" y="%d" width="91" height="32" fill="%s"/>',155+(j-1)*105,y,h)
 end
end
svg[#svg+1]='<text x="20" y="402">Design simulations only; add category text or distinct symbols/patterns.</text></g></svg>'
r.write('build/accessible/palette-review.svg',table.concat(svg,'\n'))
print('Two ramps, 1001 samples each: automatic black/white contrast >= 4.5; CVD preview generated.')
