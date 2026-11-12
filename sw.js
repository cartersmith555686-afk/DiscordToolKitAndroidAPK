const C='randomcord-v4',A=['./','./index.html','./manifest.json','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C&&x!=='rc-share').map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method==='POST'&&u.origin===location.origin&&u.pathname.endsWith('/share')){
    e.respondWith((async()=>{
      try{
        const fd=await e.request.formData();
        const c=await caches.open('rc-share');
        for(const k of await c.keys())await c.delete(k);
        const files=fd.getAll('files').filter(f=>f&&f.name);
        const meta={title:fd.get('title')||'',text:fd.get('text')||'',url:fd.get('url')||'',files:[]};
        let i=0;
        for(const f of files){
          const key='./shared-file-'+(i++);
          await c.put(key,new Response(f,{headers:{'Content-Type':f.type||'application/octet-stream','X-Name':encodeURIComponent(f.name)}}));
          meta.files.push(key)}
        await c.put('./shared-meta',new Response(JSON.stringify(meta),{headers:{'Content-Type':'application/json'}}));
      }catch(err){}
      return Response.redirect(new URL('./index.html?shared=1',self.registration.scope).href,303)})());
    return}
  if(e.request.method!=='GET'||u.origin!==location.origin)return;
  e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r}).catch(()=>caches.match(e.request).then(m=>m||caches.match('./index.html'))))});
