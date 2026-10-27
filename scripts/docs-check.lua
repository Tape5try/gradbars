-- MIT: check local documentation links and bilingual manual chapter inputs.
-- Run from the development checkout root with texlua; no network is used.
local lfs = require('lfs')
local r = dofile('scripts/release.lua')
local files = {'README.md', 'README.en.md', 'CHANGELOG.md', 'sty/README.md'}
for _, path in ipairs(r.walk('docs')) do
  if path:match('%.md$') then files[#files+1] = path end
end
local function local_target(path)
  if path:match('^%a[%w+.-]*:') or path:sub(1,1)=='#' then return nil end
  path = path:gsub('#.*$', ''):gsub('%%(%x%x)', function(h) return string.char(tonumber(h,16)) end)
  return path
end
local links = 0
for _, path in ipairs(files) do
  local content = r.read(path)
  assert(content:sub(-1)=='\n', 'Missing final newline: '..path)
  local fence = false
  for line in content:gmatch('([^\n]*)\n') do
    if line:match('^%s*```') or line:match('^%s*~~~') then
      fence = not fence
    elseif not fence then
      for target in line:gmatch('%]%(([^%)]+)%)') do
        local relative = local_target(target)
        if relative then
          local parent = path:match('^(.*)/')
          local resolved = (parent and parent..'/' or '')..relative
          assert(lfs.attributes(resolved), 'Broken documentation link: '..path..' -> '..target)
          links = links + 1
        end
      end
    end
  end
end
local chapters = 0
for _, language in ipairs({'zh-cn','en'}) do
  local manual = language=='en' and 'docs/gradbars-manual-en.tex' or 'docs/gradbars-manual.tex'
  local content = r.read(manual)
  for _, command in ipairs({'input','include'}) do
    for target in content:gmatch('\\'..command..'%{([^}]+)%}') do
      if target:match('^Chapter/') then
        assert(lfs.attributes('docs/'..target..'.tex'), 'Missing manual chapter: '..manual..' -> '..target)
        chapters = chapters+1
      end
    end
  end
end
print('Documentation references: '..links..' local links and '..chapters..' bilingual chapter inputs passed.')
