from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
book=ROOT/'Farmacias_Condor_Curso.xlsx'
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with ZipFile(book) as z:
    tabs=[n for n in z.namelist() if n.startswith('xl/tables/table') and n.endswith('.xml')]
    assert len(tabs)==18,len(tabs)
    names=[]
    for n in tabs:
        t=ET.fromstring(z.read(n));names.append(t.attrib['name'])
        assert t.find('s:autoFilter',ns) is not None,n
    assert len(names)==len(set(names))

files=[ROOT/'LEEME.md',book]
for sub in ['csv','postgresql','materiales']:
    files.extend(sorted(p for p in (ROOT/sub).rglob('*') if p.is_file()))
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(ROOT/'materiales/SHA256.json').write_text(json.dumps(hashes,indent=2,ensure_ascii=False))
files.append(ROOT/'materiales/SHA256.json')
dest=ROOT/'Farmacias_Condor_Paquete_Curso.zip'
with ZipFile(dest,'w',ZIP_DEFLATED) as z:
    for p in files:z.write(p,'Farmacias_Condor_Curso/'+str(p.relative_to(ROOT)))
with ZipFile(dest) as z:assert z.testzip() is None
print(f'Paquete: {dest}; {len(files)} archivos; {dest.stat().st_size:,} bytes')
