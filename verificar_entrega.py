"""Verifica estructura, no aprendizaje ni correccion numerica. No ejecuta codigo ajeno."""
import argparse,json,re,zipfile
from pathlib import Path,PurePosixPath

LIMIT=100*1024*1024

def revisar(path):
    path=Path(path); warnings=[]
    if path.is_file():
        if not zipfile.is_zipfile(path):raise ValueError('Se requiere carpeta o ZIP')
        z=zipfile.ZipFile(path)
        infos=[i for i in z.infolist() if not i.is_dir()]
        if sum(i.file_size for i in infos)>LIMIT:raise ValueError('ZIP supera limite de inspeccion de 100 MB descomprimidos')
        for i in infos:
            if PurePosixPath(i.filename).is_absolute() or '..' in PurePosixPath(i.filename).parts:
                raise ValueError('Ruta insegura en ZIP')
        names=[i.filename for i in infos]
        read=lambda n:z.read(n).decode('utf-8')
    else:
        if not path.is_dir():raise ValueError('Ruta inexistente')
        fs=[f for f in path.rglob('*') if f.is_file() and not f.is_symlink()]
        names=[f.relative_to(path).as_posix() for f in fs]
        read=lambda n:(path/n).read_text(encoding='utf-8')
    def has(name):return any(n==name or n.endswith('/'+name)for n in names)
    for name in ['README.md','entrega.json','USO_IA.md','BITACORA.md','informe/main.tex','informe/referencias.bib']:
        if not has(name):warnings.append('Falta '+name)
    if not any(n.endswith('.csv') and '/salidas/' in '/'+n for n in names):warnings.append('Sin CSV de salidas')
    if any(any(x in PurePosixPath(n).parts for x in ['.venv','.git','__pycache__'])for n in names):warnings.append('Incluye carpetas prescindibles')
    if any(PurePosixPath(n).name in ['.env','id_rsa','id_ed25519']for n in names):warnings.append('Posible archivo privado: retirar antes de compartir')
    for n in names:
        if n.endswith('/entrega.json') or n=='entrega.json':
            try:
                d=json.loads(read(n))
                values=' '.join(str(v)for v in d.values())
                if not re.search(r'\b[0-9a-fA-F]{40}(?:[0-9a-fA-F]{24})?\b',values):warnings.append('No se identifica hash completo en entrega.json')
                if not re.search(r'https?://',values):warnings.append('No se identifica URL de repositorio')
            except (ValueError,UnicodeError):warnings.append('entrega.json ilegible')
    return {'archivos':len(names),'advertencias':warnings,'alcance':'Revision estructural; no ejecuta codigo ni asigna nota.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('ruta');p.add_argument('--json',action='store_true');a=p.parse_args()
    try:
        r=revisar(a.ruta)
        if a.json:print(json.dumps(r,ensure_ascii=False,indent=2))
        else:
            print(r['alcance']);print('Archivos:',r['archivos'])
            for w in r['advertencias']:print('REVISAR:',w)
            if not r['advertencias']:print('Estructura sin advertencias; falta revision tecnica.')
    except (OSError,ValueError,zipfile.BadZipFile) as exc:raise SystemExit(str(exc))
