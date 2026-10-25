-- MIT: inspect actual Tagged PDF objects with TeX Live's pdfe library.
local M={}
function M.snapshot(path)
  local d=assert(pdfe.open(path),'Cannot open '..path)
  local function resolve(t,v)
    while t==10 do t,v=pdfe.getfromreference(v) end
    return t,v
  end
  local function get(dict,key) return resolve(pdfe.getfromdictionary(dict,key)) end
  local root=pdfe.getdictionary(pdfe.getcatalog(d),'StructTreeRoot')
  if not root then pdfe.close(d); return '' end
  local result,seen={},{}
  local function canonical(s) return tostring(s):gsub('ID%.0*(%d+)','ID.%1') end
  local function attributes(t,v)
    t,v=resolve(t,v)
    if t==8 then
      local parts={}
      for _,key in ipairs({'Scope','RowSpan','ColSpan'}) do
        local _,value=get(v,key)
        if value~=nil then parts[#parts+1]=key..'='..tostring(value) end
      end
      local ht,hv=get(v,'Headers')
      if ht==7 then
        local ids={}
        for _,item in ipairs(pdfe.arraytotable(hv)) do local _,id=resolve(table.unpack(item));ids[#ids+1]=canonical(id) end
        parts[#parts+1]='Headers='..table.concat(ids,'&')
      end
      return table.concat(parts,',')
    elseif t==7 then
      local parts={}
      for _,item in ipairs(pdfe.arraytotable(v)) do parts[#parts+1]=attributes(table.unpack(item)) end
      return table.concat(parts,';')
    end
    return ''
  end
  local function walk(t,v)
    t,v=resolve(t,v)
    if t==7 then
      for _,item in ipairs(pdfe.arraytotable(v)) do walk(table.unpack(item)) end
    elseif t==8 and not seen[tostring(v)] then
      seen[tostring(v)]=true
      local _,s=get(v,'S')
      if s=='Figure' or s=='Table' or s=='TR' or s=='TH' or s=='TD' or s=='Caption' or s=='P' then
        local _,alt=get(v,'Alt');alt=alt or ''
        local pt,parent=get(v,'P');local parentrole=''
        if pt==8 then local _,role=get(parent,'S');parentrole=role or '' end
        local _,id=get(v,'ID');id=id or ''
        result[#result+1]=s..'|'..alt..'|'..attributes(pdfe.getfromdictionary(v,'A'))..'|parent='..parentrole..'|ID='..canonical(id)
      end
      walk(pdfe.getfromdictionary(v,'K'))
    end
  end
  walk(8,root);table.sort(result);pdfe.close(d)
  return table.concat(result,'\n')
end
return M
