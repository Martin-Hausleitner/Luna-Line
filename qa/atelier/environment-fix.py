"""Bounded browser-test environment correction; no application changes."""
from pathlib import Path
import hashlib
p = Path('qa/atelier/run-qa.py')
s = p.read_text()
assert hashlib.sha256(s.encode()).hexdigest() == '7dcaa064d0bc3324edbeaf4e09755f75e0be0afdf00e94850f9be32cbe2a4d03'
old = "launch={'headless':True,'args':['--no-sandbox','--enable-unsafe-webgpu','--use-angle=swiftshader','--enable-features=Vulkan','--disable-vulkan-surface']}"
new = "launch={'headless':not bool(__import__('os').environ.get('LUNA_HEADED')),'args':['--no-sandbox','--enable-unsafe-webgpu','--enable-features=Vulkan','--use-angle=vulkan','--use-vulkan=swiftshader','--use-webgpu-adapter=swiftshader','--disable-vulkan-surface','--disable-dev-shm-usage','--disable-gpu-watchdog']}"
assert old in s
s = s.replace(old, new)
s = s.replace("def screenshot(name):\n        settle(180)", "def screenshot(name):\n        if args.require_webgpu and name!='08-fallback.png': check('WebGPU remains active for '+name,'Luna.gpu.mode===\"webgpu\"&&!Luna.gpu.error')\n        settle(180)")
assert hashlib.sha256(s.encode()).hexdigest() == 'e8aecfc68b8ede9545d0612966555a92806369a8befcbcecc22faee3a8981dc9'
p.write_text(s)
