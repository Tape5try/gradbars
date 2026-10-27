-- MIT: create the runtime directory and run docstrip without shell escape.
-- Run from the source package root: texlua scripts/unpack.lua
local lfs = require('lfs')
local function exists(path)
  local f = io.open(path, 'rb')
  if f then f:close(); return true end
  return false
end
assert(exists('gradbars.ins') and exists('gradbars.dtx'),
  'Run texlua scripts/unpack.lua from the directory containing gradbars.ins/dtx')
if not lfs.symlinkattributes('sty') then assert(lfs.mkdir('sty')) end
assert(lfs.attributes('sty', 'mode') == 'directory', 'sty must be a directory')
if not lfs.symlinkattributes('sty/README.md') then
  local f = assert(io.open('sty/README.md', 'wb'))
  f:write('# Extracted runtime modules\n\n',
    'Run texlua scripts/unpack.lua from the parent directory to regenerate.\n')
  f:close()
end
assert(lfs.attributes('sty/README.md', 'mode') == 'file', 'sty/README.md must be a file')
local ok, _, code = os.execute('tex -interaction=nonstopmode -halt-on-error gradbars.ins')
if ok ~= true and ok ~= 0 then os.exit(code or 1) end
local n = 0
for name in lfs.dir('sty') do if name:match('%.sty$') then n = n + 1 end end
assert(n == 22, 'Expected 22 extracted modules in sty/, found ' .. n)
print('Extracted 22 runtime modules into sty/.')
