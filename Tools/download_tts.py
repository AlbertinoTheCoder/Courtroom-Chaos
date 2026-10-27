import urllib.request,pathlib,time,concurrent.futures
root=pathlib.Path(__file__).resolve().parents[1]/'Saved'/'TTS'/'models';root.mkdir(parents=True,exist_ok=True)
urls={
 'kokoro-v1.0.onnx':'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx',
 'voices-v1.0.bin':'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin'}
def download(item):
 name,url=item;p=root/name
 if not p.exists():
  with urllib.request.urlopen(url+'?download=1&t='+str(int(time.time())),timeout=90) as r,p.with_suffix('.download').open('wb') as f:
   while chunk:=r.read(1024*1024):f.write(chunk)
  p.with_suffix('.download').replace(p)
 print(name,p.stat().st_size,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(download,urls.items()))
