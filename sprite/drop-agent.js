/* ============================================================
   DropAgent — the sprite runtime. ONE COPY LIVES ON EVERY DEVICE.
   Include it on any page and that page becomes a Koda Kai station:
   Drop floats on, listens on the HQ bus, and executes commands with
   visible, Bluey-grade animation. Then he reports home.

   Bus today: BroadcastChannel (real cross-tab). Tomorrow: WebSocket
   to the HQ sync server on Shadow — same message shape, no rewrite.
   ============================================================ */
(function(){
"use strict";
var ART_DEFAULT='assets/char/drop-toy3d.webp';

/* base styling travels with the runtime — one <script> turns any page
   into a station, no extra CSS needed */
(function css(){
  if(document.getElementById('drop-agent-css')) return;
  var s=document.createElement('style'); s.id='drop-agent-css';
  s.textContent=
   '.drop-agent{position:absolute;width:84px;z-index:9999;pointer-events:none;transform:translate(-50%,-50%);}'+
   '.drop-agent img{width:100%;display:block;filter:drop-shadow(0 8px 16px rgba(0,0,0,.35));}'+
   '.drop-bub{position:absolute;bottom:105%;left:50%;transform:translateX(-50%);background:#fff;color:#0a2233;'+
   'font:700 14px -apple-system,system-ui,sans-serif;padding:8px 12px;border-radius:12px;white-space:nowrap;'+
   'box-shadow:0 4px 14px rgba(0,0,0,.25);}';
  document.head.appendChild(s);
})();

/* ---------------- HQ bus (pluggable transport) ---------------- */
function DropBus(name){
  this.handlers=[];
  try{ this.ch=new BroadcastChannel(name||'koda-hq'); }
  catch(e){ this.ch=null; }
  var self=this;
  if(this.ch) this.ch.onmessage=function(e){ self.handlers.forEach(function(h){ h(e.data); }); };
}
DropBus.prototype.send=function(msg){ if(this.ch){ try{ this.ch.postMessage(msg); }catch(e){} } };
DropBus.prototype.onMsg=function(h){ this.handlers.push(h); };

/* ---------------- Bluey-grade motion ----------------
   squash & stretch · anticipation · follow-through · blink.
   Every move is physics, not slides. */
function easeIO(t){ return t<.5 ? 2*t*t : 1-Math.pow(-2*t+2,2)/2; }
function animate(dur,fn){
  return new Promise(function(res){ var t0=performance.now();
    (function f(){ var t=Math.min(1,(performance.now()-t0)/dur); fn(easeIO(t));
      if(t<1) requestAnimationFrame(f); else res(); })();
  });
}

/* ---------------- the sprite ---------------- */
function DropAgent(station,mountEl,opts){
  opts=opts||{};
  this.station=station;
  this.bus=opts.bus||new DropBus();
  this.onAction=opts.onAction||function(){};
  var wrap=document.createElement('div'); wrap.className='drop-agent';
  var img=document.createElement('img'); img.src=opts.art||ART_DEFAULT; img.alt='Drop';
  img.draggable=false; wrap.appendChild(img);
  var bub=document.createElement('div'); bub.className='drop-bub'; bub.style.display='none';
  wrap.appendChild(bub);
  (mountEl||document.body).appendChild(wrap);
  this.el=wrap; this.img=img; this.bub=bub;
  this.x=50; this.y=50; this.blinking=false;
  this.place(50,50);
  var self=this;
  this.bus.onMsg(function(m){ if(m && m.to===self.station && m.type==='cmd') self.execute(m); });
  this.blinkLoop();
}
DropAgent.prototype.place=function(x,y){
  this.x=x; this.y=y;
  this.el.style.left=x+'%'; this.el.style.top=y+'%';
};
/* swim along an arc, body stretching with the motion */
DropAgent.prototype.swimTo=function(x2,y2,dur){
  var self=this, x1=this.x, y1=this.y, lift=16;
  this.img.style.transition='transform .16s';
  this.img.style.transform='scaleY(.8) scaleX(1.14)'; /* anticipation crouch */
  return new Promise(function(r){ setTimeout(r,170); }).then(function(){
    self.img.style.transition='';
    return animate(dur||950,function(t){
      var x=x1+(x2-x1)*t, y=y1+(y2-y1)*t-Math.sin(t*Math.PI)*lift;
      self.place(x,y);
      var s=1+Math.sin(t*Math.PI)*.2; /* squash & stretch */
      self.img.style.transform='scaleY('+s.toFixed(3)+') scaleX('+(1/Math.sqrt(s)).toFixed(3)+')';
    });
  }).then(function(){ /* follow-through */
    self.img.style.transition='transform .28s';
    self.img.style.transform='scaleY(.88) scaleX(1.08)';
    return new Promise(function(r){ setTimeout(function(){
      self.img.style.transform=''; self.img.style.transition=''; r(); },300); });
  });
};
DropAgent.prototype.blinkLoop=function(){
  var self=this;
  (function blink(){
    if(!self.blinking){ self.blinking=true;
      self.img.style.transition='transform .09s';
      self.img.style.transform='scaleY(.07)';
      setTimeout(function(){ self.img.style.transform=''; self.img.style.transition='';
        self.blinking=false; },140);
    }
    setTimeout(blink,2400+Math.random()*2800);
  })();
};
DropAgent.prototype.trick=function(){ /* the arrival spin */
  var self=this;
  return animate(620,function(t){
    self.img.style.transform='rotate('+(t*360)+'deg) scale('+(1+Math.sin(t*Math.PI)*.16)+')';
  }).then(function(){ self.img.style.transform=''; });
};
DropAgent.prototype.happy=function(){
  var self=this;
  return animate(500,function(t){
    self.img.style.transform='translateY('+(-Math.sin(t*Math.PI)*22)+'px) scaleY('+(1+Math.sin(t*Math.PI)*.1)+')';
  }).then(function(){ self.img.style.transform=''; });
};
DropAgent.prototype.speak=function(text,ms){
  var self=this; this.bub.textContent=text; this.bub.style.display='block';
  clearTimeout(this._bubT);
  this._bubT=setTimeout(function(){ self.bub.style.display='none'; },ms||2400);
};
/* a command arrived from HQ: announce, do it visibly, report home */
DropAgent.prototype.execute=function(msg){
  var self=this;
  this.speak('On it! ✨');
  return Promise.resolve(this.onAction(msg.action,msg.params||{},msg))
    .then(function(){ return self.trick(); })
    .then(function(){ self.speak('Done! ✔'); self.bus.send(
      {to:msg.from,type:'done',action:msg.action,station:self.station}); });
};
/* send a command to another station */
DropAgent.prototype.send=function(to,action,params){
  this.bus.send({to:to,from:this.station,type:'cmd',action:action,params:params||{}});
};

window.DropAgent=DropAgent;
window.DropBus=DropBus;
})();
