-- MIT: isolated extraction and CTAN archive regressions; run with texlua.
-- Generate gradbars.dtx/ins first. No development source or runtime is changed.
local lfs = require('lfs')
local r = dofile('scripts/release.lua')
local version = r.metadata()
local ctan_readme = r.ctan_readme('README.en.md')
local fixture = {}
for _,name in ipairs({'gradbars.dtx','gradbars.ins','build.lua','scripts/release.lua',
  'scripts/unpack.lua','docs/examples/precision-recall.tex'}) do fixture[name]=r.read(name) end
local previous = lfs.currentdir()
local work = os.tmpname()
os.remove(work)
assert(lfs.mkdir(work));assert(lfs.chdir(work))

local checks = 0
local function expect_failure(action, diagnostic)
  local ok,err=pcall(action)
  assert(not ok and tostring(err):find(diagnostic,1,true),
    'Expected '..diagnostic..', got '..tostring(err))
  checks=checks+1
end
local function execute(command, diagnostic)
  local ok,_,code=os.execute(command..' > run.stdout 2>&1')
  if diagnostic then
    assert(ok~=true and ok~=0, 'Expected command failure: '..command)
    assert(r.read('run.stdout'):gsub('%s+',' '):find(diagnostic,1,true),
      'Wrong command diagnostic: '..command)
  else assert(ok==true or ok==0, command..' failed ('..tostring(code)..'); inspect '..work) end
  checks=checks+1
end

-- Stored ZIP fixtures let the validator reject bad metadata without depending
-- on an external zip program or changing the system clock/permissions.
local crc_table={}
for n=0,255 do
  local c=n
  for _=1,8 do c=(c >> 1) ~ ((c & 1)==1 and 0xedb88320 or 0) end
  crc_table[n]=c
end
local function crc32(body)
  local c=0xffffffff
  for i=1,#body do c=(c >> 8) ~ crc_table[(c ~ body:byte(i)) & 255] end
  return (~c) & 0xffffffff
end
local date=((2026-1980) << 9) | (10 << 5) | 27
local function makezip(entries, comment)
  local chunks,central,offset={},{},0
  for _,entry in ipairs(entries) do
    local name,body=entry.name,entry.body or ''
    local day=entry.date or date
    local mode=entry.mode or (name:sub(-1)=='/' and 16877 or 33188)
    local crc=crc32(body)
    local localname=entry.localname or name
    local header='PK\003\004'..string.pack('<I2I2I2I2I2I4I4I4I2I2',
      20,0,0,0,entry.localdate or day,crc,#body,#body,#localname,0)..localname..body
    chunks[#chunks+1]=header
    central[#central+1]='PK\001\002'..string.pack('<I2I2I2I2I2I2I4I4I4I2I2I2I2I2I4I4',
      788,20,0,0,0,day,crc,#body,#body,#name,0,0,0,0,mode << 16,offset)..name
    offset=offset+#header
  end
  local directory=table.concat(central)
  comment=comment or ''
  r.write('fixture.zip',table.concat(chunks)..directory..'PK\005\006'
    ..string.pack('<I2I2I2I2I4I4I2',0,0,#entries,#entries,#directory,offset,#comment)..comment)
end
local function base()
  local entries={{name='gradbars/'}}
  local files={
    ['README.md']='CTAN entry with MIT and adapted-example license scope.',
    ['LICENSE']='MIT License fixture',
    ['gradbars.dtx']='\\ProvidesPackage{gradbars}[2026/10/27 v'..version..' fixture]',
    ['gradbars.ins']='docstrip fixture', ['build.lua']='native build fixture',
    ['scripts/release.lua']='release fixture', ['scripts/unpack.lua']='unpack fixture',
    ['docs/examples/precision-recall.tex']=fixture['docs/examples/precision-recall.tex']}
  for _,stem in ipairs({'gradbars-manual','gradbars-manual-en','gradbars-source'}) do
    files[stem..'-v'..version..'.pdf']='%PDF fixture '..stem
  end
  local names={};for name in pairs(files) do names[#names+1]=name end;table.sort(names)
  for _,name in ipairs(names) do entries[#entries+1]={name='gradbars/'..name,body=files[name]} end
  return entries
end
local function reject(entry, diagnostic)
  local entries=base();entries[#entries+1]=entry;makezip(entries)
  expect_failure(function() r.verify('fixture.zip') end,diagnostic)
end
-- Metadata is read from the local documented source, just as for real builds.
r.write('gradbars.dtx',fixture['gradbars.dtx'])
makezip(base(),'ordinary archive comment');r.verify('fixture.zip');checks=checks+1
local withmarker=base()
withmarker[#withmarker+1]={name='gradbars/sty/'}
withmarker[#withmarker+1]={name='gradbars/sty/README.md',body='Optional extraction marker'}
makezip(withmarker);r.verify('fixture.zip');checks=checks+1
local doclayout=base()
for _,entry in ipairs(doclayout) do
  entry.name=entry.name:gsub('^gradbars/(gradbars[^/]+)%-v'..version:gsub('%.','%%.')..'%.pdf$',
    'gradbars/docs/%1.pdf')
end
makezip(doclayout);r.verify('fixture.zip');checks=checks+1
for _,name in ipairs({'gradbars/../escape.tex','gradbars/docs/.hidden.tex',
  'gradbars/docs/with space.tex','gradbars/docs//double.tex','gradbars/docs/a\\b.tex',
  'gradbars/docs/中文.tex'}) do
  reject({name=name,body='unsafe path '..name},'Unsafe archive path')
end
reject({name='gradbars/tests/check.lua',body='development fixture'},'Development file in archive')
reject({name='gradbars/docs/releases/old.md',body='old release'},'Development file in archive')
reject({name='gradbars/ROADMAP.md',body='local roadmap'},'Local maintenance file in archive')
reject({name='gradbars/docs/cache.py',body='python fixture'},'Python in archive')
reject({name='gradbars/docs/manual.aux',body='temporary fixture'},'Temporary file in archive')
reject({name='gradbars/docs/manual.LOG',body='uppercase temporary fixture'},'Temporary file in archive')
reject({name='gradbars/sty/gradbars.sty',body='generated fixture'},'Generated file in source archive')
reject({name='gradbars/gradbars.sty',body='root generated fixture'},'Generated file in source archive')
reject({name='gradbars/docs/example.tex',body='bad mode',mode=33261},'Bad archive permissions')
reject({name='gradbars/docs/',mode=16804},'Bad archive permissions')
reject({name='gradbars/docs/link.tex',body='symlink',mode=41471},'Bad archive permissions')
reject({name='gradbars/docs/date.tex',body='bad date',date=33},'Missing/default ZIP timestamp')
reject({name='gradbars/docs/date.tex',body='zero date',date=0},'Missing/default ZIP timestamp')
reject({name='gradbars/docs/date.tex',body='bad calendar date',date=((2026-1980) << 9) | (2 << 5) | 31},'Missing/default ZIP timestamp')
reject({name='gradbars/docs/header.tex',body='mismatched local name',localname='gradbars/docs/other.tex'},'Conflicting ZIP local header')
reject({name='gradbars/README.md',body='repeated path'},'Duplicate archive path')
reject({name='gradbars/readme.md',body='case collision'},'Duplicate archive path')
reject({name='gradbars/docs/build.lua',body='repeated basename'},'Repeated filename')
reject({name='gradbars/docs/copy.md',body='native build fixture'},'Duplicate contents')
local entries=base()
for _,entry in ipairs(entries) do
  if entry.name:match('/precision%-recall%.tex$') then entry.body='unattributed example' end
end
makezip(entries);expect_failure(function() r.verify('fixture.zip') end,'Missing adapted-example attribution')
r.write('source.txt','timestamp fixture');assert(lfs.touch('source.txt',1234567890,1234567890))
r.copy('source.txt','copied.txt')
assert(lfs.attributes('copied.txt','modification')==1234567890,'Copy changed source modification time')
checks=checks+1
assert(r.license_note:find('Only the attributed table data',1,true),'License scope missing')
assert(ctan_readme:find('l3build unpack\nl3build doc',1,true)
  and not ctan_readme:find('```sh\nl3build check',1,true)
  and ctan_readme:find('CC BY-SA 4.0',1,true), 'Incorrect CTAN rebuild/license instructions')
checks=checks+1
local environment=setmetatable({
  fileexists=function(name) return name=='gradbars.dtx' or name=='gradbars.ins' end,
  direxists=function() return false end,
  dofile=function(name) assert(name=='scripts/release.lua');return r end,
  target_list={check={},bundlecheck={}},
  os=setmetatable({getenv=function(name) if name=='CTAN_NOTE' then return 'Maintainer note fixture' end end}, {__index=os})
}, {__index=_G})
assert(load(fixture['build.lua'],'@build.lua','t',environment))()
assert(environment.uploadconfig.license[1]=='mit' and environment.uploadconfig.license[2]=='cc-by-sa-4'
  and environment.uploadconfig.note:find(r.license_note,1,true)
  and environment.uploadconfig.note:find('Maintainer note fixture',1,true)
  and not environment.ctanupload, 'Upload license scope, maintainer note or opt-in changed')
checks=checks+1

-- Real docstrip and l3build must repair a missing directory/marker, while bare
-- TeX must fail early with the documented command instead of writing at root.
for name,body in pairs(fixture) do
  if not name:match('^docs/') then r.write('project/'..name,body) end
end
assert(lfs.chdir('project'))
local function no_root_modules()
  for name in lfs.dir('.') do assert(not name:match('%.sty$'),'Root runtime module: '..name) end
end
local function modules(dir)
  local n=0
  for name in lfs.dir(dir) do if name:match('%.sty$') then n=n+1 end end
  assert(n==22,'Incomplete extraction in '..dir);no_root_modules()
end
execute('tex -interaction=nonstopmode -halt-on-error gradbars.ins','Run texlua scripts/unpack.lua')
execute('texlua scripts/unpack.lua');modules('sty')
assert(os.remove('sty/README.md'))
execute('tex -interaction=nonstopmode -halt-on-error gradbars.ins','Run texlua scripts/unpack.lua')
execute('texlua scripts/unpack.lua');modules('sty')
for name in lfs.dir('sty') do if name~='.' and name~='..' then assert(os.remove('sty/'..name)) end end
assert(lfs.rmdir('sty'))
execute('l3build unpack');modules('build/l3build/unpacked/sty')
execute('l3build check','Development tests are absent')
no_root_modules()
assert(lfs.chdir(previous))
print('Maintenance regressions passed: '..checks..' checks; isolated files: '..work)
