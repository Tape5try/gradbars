-- MIT: reproducible, bounded performance measurements using the installed TeX engines.
local lfs = require('lfs')
local r = dofile('scripts/release.lua')
local root = lfs.currentdir():gsub('\\','/')
local opt = {runtime='sty', output='build/benchmark/current', runs=3, rows=120, groups=12}
local engines = {}
for _, a in ipairs(arg) do
  local k, v = a:match('^%-%-([a-z]+)=(.+)$')
  if k then assert(opt[k] ~= nil, 'Unknown option: '..k); opt[k] = v
  else
    assert(a=='pdflatex' or a=='xelatex' or a=='lualatex', 'Unknown engine: '..a)
    engines[#engines+1] = a
  end
end
if #engines==0 then engines={'pdflatex','xelatex','lualatex'} end
for _, k in ipairs({'runs','rows','groups'}) do
  opt[k] = assert(tonumber(opt[k]), 'Invalid '..k)
  assert(opt[k]%1==0, 'Expected integer '..k)
end
assert(opt.runs>=2 and opt.runs<=10, 'runs must be 2..10')
assert(opt.rows>=12 and opt.rows<=600, 'rows must be 12..600')
assert(opt.groups>=1 and opt.groups<=opt.rows, 'groups must be 1..rows')
assert(not opt.output:match('^/') and not opt.output:find('..',1,true)
  and opt.output:match('^[%w_./%-]+$'), 'Use a relative output directory without traversal')
local function quote(s)
  if os.type=='windows' then
    assert(not s:find('["%%!\r\n]'),'Unsupported shell character in path')
    return '"'..s..'"'
  end
  return "'"..s:gsub("'", "'\\''").."'"
end
local snapshot=opt.output..'/runtime'
local hashes={}
for _, p in ipairs(r.walk(opt.runtime)) do
  if p:match('%.sty$') then
    local name=p:match('[^/]+$')
    r.copy(p,snapshot..'/'..name)
    hashes[#hashes+1]=name..' '..md5.sumhexa(r.read(p))
  end
end
assert(#hashes==23,'Expected a complete 23-module runtime')
local csv={'Name,Group,High,Low,Other'}
for i=1,opt.rows do
  csv[#csv+1]=string.format('S%d,G%d,%s,%s,%s',i,math.floor((i-1)*opt.groups/opt.rows)+1,
    i%13==0 and 'NA' or tostring((i*7)%101),
    i%17==0 and 'NA' or tostring((i*3)%101), tostring(i%5))
end
local data=table.concat(csv,'\n')..'\n'
r.write(opt.output..'/data.csv',data)
local tex=[=[
\documentclass{article}
\usepackage[margin=15mm]{geometry}
\usepackage{gradbars}
\usegradbarslibrary{distribution}
\gradbarsloadcsv{bench}{data.csv}
\ExplSyntaxOn
\int_new:N\g__bench_start_int
\cs_new_protected:Npn\benchStart{\int_gset:Nn\g__bench_start_int{\sys_timer:}}
\cs_new_protected:Npn\benchStop#1
 {\iow_term:x{GBENCH|#1|\int_eval:n{\sys_timer:-\g__bench_start_int}}}
\cs_new_eq:NN\benchRank\gradtableRank
\cs_set_protected:Npn\gradtableRank
 {\benchStart\prg_replicate:nn{5}{\benchRank}\benchStop{rank-5}}
\cs_new_eq:NN\benchScan\gradtableScan
\cs_set_protected:Npn\gradtableScan{\benchStart\benchScan\benchStop{measure}}
\ExplSyntaxOff
\begin{document}
\ExplSyntaxOn
\benchStart
\prg_replicate:nn{1000}{\gradbarsparsenumber{1234.5}{\benchNumber}}
\benchStop{parse-1000}
\benchStart
\prg_replicate:nn{20}{\group_begin:
 \__gradbars_distribution_parse:n{0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
  16,17,18,19,20,21,22,23,24,25,26,27,28,29,NA,100}\group_end:}
\benchStop{stats-20}
\benchStart
\prg_replicate:nn{20}{\hbox_set:Nn\l_tmpa_box{\gradbar[label=none,width=20mm]{42}}}
\benchStop{bar-total-20}
\ExplSyntaxOff
\begin{gradtable}[data=bench,group by=group,rank scope=group,long=true]
\gradcolumn[source=Name,width=15mm]{name}{Service}
\gradcolumn[source=Group,width=12mm]{group}{Group}
\gradcolumn[source=High,type=number,mark=both,width=18mm]{high}{Higher}
\gradcolumn[source=Low,type=number,mark=both,options={better=lower},width=18mm]{low}{Lower}
\gradcolumn[source=Other,type=number,mark=both,width=18mm]{other}{Repeated}
\end{gradtable}
\end{document}
]=]
r.write(opt.output..'/benchmark.tex',tex)
r.write(opt.output..'/snapshot.txt',table.concat(hashes,'\n')..'\ndata '..md5.sumhexa(data)..'\n')
local report={'engine,run,process_state,phase,seconds'}
local summary={'# Performance measurement', '',
  'Runtime: '..opt.runtime..'; rows: '..opt.rows..'; groups: '..opt.groups..'; runs: '..opt.runs..'.',
  'Source/data MD5 identities: snapshot.txt. Samples: measurements.csv.',
  'First process versus subsequent processes; OS/font caches are NOT flushed.',
  'TeX elapsed timer (65536 ticks/s); no process startup or OS memory metric.',
  'rank-5 repeats ranking five times. bar-total-20 includes parsing/layout/TikZ, not pure drawing.',
  'Phase values have different workloads and must not be summed or compared as shares.', '',
  '| Engine | Phase | First (s) | Subsequent median (s) |', '| --- | --- | --- | --- |'}
local previous_input=os.getenv('TEXINPUTS') or ''
local previous_var=os.getenv('TEXMFVAR')
local previous_cache=os.getenv('TEXMFCACHE')
r.write(opt.output..'/tex-cache/.keep','')
local sep=os.type=='windows' and ';' or ':'
os.setenv('TEXINPUTS',root..'/'..snapshot..sep..root..'/'..opt.output..sep..previous_input)
os.setenv('TEXMFVAR',root..'/'..opt.output..'/tex-cache')
os.setenv('TEXMFCACHE',root..'/'..opt.output..'/tex-cache')
for _, engine in ipairs(engines) do
  local version_ok=os.execute(engine..' --version > '..quote(opt.output..'/'..engine..'-version.txt')..' 2>&1')
  assert(version_ok==true or version_ok==0,'Cannot identify engine: '..engine)
  local values={}
  for run=1,opt.runs do
    local job=engine..'-'..run
    local cmd=engine..' -interaction=nonstopmode -halt-on-error -no-shell-escape -jobname='..job
      ..' -output-directory='..quote(opt.output)..' '..quote(opt.output..'/benchmark.tex')
      ..' > '..quote(opt.output..'/'..job..'.stdout')..' 2>&1'
    local ok,_,code=os.execute(cmd)
    assert(ok==true or ok==0,'Compile failed: '..job..' (exit '..tostring(code)..'); see stdout')
    local found=0
    for phase,ticks in r.read(opt.output..'/'..job..'.log'):gmatch('GBENCH|([%w%-]+)|(%d+)') do
      local seconds=tonumber(ticks)/65536
      values[phase]=values[phase] or {}; values[phase][run]=seconds
      report[#report+1]=string.format('%s,%d,%s,%s,%.6f',engine,run,
        run==1 and 'first' or 'subsequent',phase,seconds)
      found=found+1
    end
    assert(found==5,'Missing phase samples: '..job)
    print(engine..' run '..run..'/'..opt.runs..' complete')
  end
  for _,phase in ipairs({'parse-1000','stats-20','bar-total-20','rank-5','measure'}) do
    local warm={table.unpack(values[phase],2)}; table.sort(warm)
    local middle=math.floor((#warm+1)/2)
    local median=#warm%2==1 and warm[middle] or (warm[middle]+warm[middle+1])/2
    summary[#summary+1]=string.format('| %s | %s | %.6f | %.6f |',engine,phase,values[phase][1],median)
  end
end
os.setenv('TEXINPUTS',previous_input)
os.setenv('TEXMFVAR',previous_var or '')
os.setenv('TEXMFCACHE',previous_cache or '')
r.write(opt.output..'/measurements.csv',table.concat(report,'\n')..'\n')
r.write(opt.output..'/results.md',table.concat(summary,'\n')..'\n')
print('Results: '..opt.output..'/results.md')
