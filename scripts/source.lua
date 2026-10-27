-- MIT: gradbars documented-source generator; run with texlua, no Python needed.
local lfs = require('lfs')
local function read(path)
  local f = assert(io.open(path, 'rb')); local s = f:read('*a'); f:close()
  s = s:gsub('\r\n', '\n'):gsub('\r', '\n'):gsub('[ \t]+\n', '\n')
  return s:gsub('\n*$', '') .. '\n'
end
local entry = read('sty/gradbars.sty')
local date, version = entry:match('\\ProvidesPackage{gradbars}%[([%d/]+) v([%d.]+)')
assert(date and version, 'Missing package metadata')
local names = {}
for name in lfs.dir('sty') do if name:match('%.sty$') then names[#names+1] = name end end
table.sort(names)
local dtx = {'% \\iffalse', '%<*driver>', '\\documentclass{l3doc}',
  '\\OnlyDescription', '\\begin{document}', '\\DocInput{gradbars.dtx}',
  '\\end{document}', '%</driver>', '% \\fi',
  '% \\title{\\textsf{gradbars}: documented source}',
  '% \\author{SuFan (Tape5try)}', '% \\date{v' .. version .. ' / ' .. date .. '}',
  '% \\maketitle', '% \\input{docs/source-guide.tex}', '% \\StopEventually{}'}
local ins = {
  '\\newread\\gradbarsDirectoryCheck',
  '\\openin\\gradbarsDirectoryCheck=sty/README.md',
  '\\ifeof\\gradbarsDirectoryCheck',
  '  \\errmessage{Missing sty/README.md directory marker. Run texlua scripts/unpack.lua to create or repair sty/ and extract the modules}',
  '  \\expandafter\\end',
  '\\fi', '\\closein\\gradbarsDirectoryCheck',
  '% Plain TeX cannot create directories; the Lua entry repairs missing markers.',
  '\\def\\WriteToDir{sty/}', '\\input docstrip.tex',
  '\\keepsilent', '\\askforoverwritefalse', '\\nopreamble', '\\nopostamble', '\\generate{'}
for _, name in ipairs(names) do
  local stem = name:gsub('%.sty$', '')
  local tag = stem == 'gradbars' and 'entry' or stem:gsub('^gradbars%-', '')
  dtx[#dtx+1] = '% \\section{\\texttt{' .. name .. '}}'
  dtx[#dtx+1] = '%    \\begin{macrocode}'
  for line in read('sty/' .. name):gmatch('(.-)\n') do
    dtx[#dtx+1] = '%<' .. tag .. '>' .. line
  end
  dtx[#dtx+1] = '%    \\end{macrocode}'
  ins[#ins+1] = '  \\file{' .. name .. '}{\\from{gradbars.dtx}{' .. tag .. '}}'
end
ins[#ins+1] = '}'; ins[#ins+1] = '\\endbatchfile'
for name, lines in pairs({['gradbars.dtx']=dtx, ['gradbars.ins']=ins}) do
  local content = table.concat(lines, '\n') .. '\n'
  if arg[1] == '--check' then
    assert(read(name) == content, 'Stale ' .. name .. '; run texlua scripts/source.lua')
  else
    local f = assert(io.open(name, 'wb')); f:write(content); f:close()
  end
end
print('Documented sources match ' .. #names .. ' runtime modules.')
