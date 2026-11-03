-- MIT: independent dense sRGB reference for actual rendered label-box geometry.
-- Run after scripts/check.lua; bounds may be conservative, never optimistic.
local r = dofile('scripts/release.lua')
local function linear(c)
  if c <= .04045 then return c/12.92 end
  return ((c+.055)/1.055)^2.4
end
local function luminance(rgb)
  return .2126*linear(rgb[1])+.7152*linear(rgb[2])+.0722*linear(rgb[3])
end
for _,engine in ipairs({'pdflatex','xelatex','lualatex'}) do
  local log=r.read('build/native-check/'..engine..'/v120-contrast-gradients.stdout')
  local count=0
  for name,lo,hi,a,b,black,white in log:gmatch('AREA%-REFERENCE|([%a]+)|([^|]+)|([^|]+)|([^|]+)|([^|]+)|([^|]+)|([^%s]+)') do
    lo,hi,a,b,black,white=tonumber(lo),tonumber(hi),tonumber(a),tonumber(b),tonumber(black),tonumber(white)
    assert(lo and hi and a and b and black and white,'Malformed reference record')
    local minimum,maximum=1,0
    for i=0,10000 do
      local t=a+(b-a)*i/10000
      local rgb
      if name=='opposing' then rgb={1-t,0,t}
      elseif name=='reverse' then rgb={1-t,1-t,1-t}
      elseif name=='band' then local c=t<.5 and .5 or 1;rgb={c,c,c}
      else rgb={t,t,t} end
      local value=luminance(rgb)
      minimum=math.min(minimum,value);maximum=math.max(maximum,value)
    end
    -- The large glyph box protrudes vertically beyond the track onto white.
    if name=='large' then maximum=1 end
    assert(lo<=minimum+.0001 and hi>=maximum-.0001,engine..'/'..name..': optimistic bound')
    assert(minimum-lo<.02 and hi-maximum<.02,engine..'/'..name..': excessively loose bound')
    assert(math.abs(black-(lo+.05)/.05)<.00001,engine..'/'..name..': black ratio')
    assert(math.abs(white-1.05/(hi+.05))<.00001,engine..'/'..name..': white ratio')
    count=count+1
  end
  assert(count==6,engine..': expected six area references')
  print(engine..': six label-area bounds enclose independent 10,001-point references.')
end
