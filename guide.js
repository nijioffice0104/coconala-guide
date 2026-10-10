(function(){
  // 別のステップに移ったら、前のページのスクロール位置を引き継がず先頭から表示する
  try{history.scrollRestoration='manual'}catch(e){}
  function toTop(){if(!location.hash)window.scrollTo(0,0)}
  toTop();
  window.addEventListener('load',function(){toTop();setTimeout(toTop,150)});
  window.addEventListener('pageshow',toTop);

  var KEY='niji-coconala-guide-v2';
  var state={};
  try{state=JSON.parse(localStorage.getItem(KEY)||'{}')||{}}catch(e){state={}}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}}

  // 宿題のチェックと記入欄（このブラウザの中だけに保存）
  function update(){
    document.querySelectorAll('[data-progress]').forEach(function(p){
      var all=document.querySelectorAll('[data-group="'+p.dataset.progress+'"] input');
      var done=[].filter.call(all,function(i){return i.checked}).length;
      p.textContent=done===all.length?'このステップの宿題はすべて完了です':'完了 '+done+' / '+all.length;
    });
  }
  document.querySelectorAll('.check input[type=checkbox]').forEach(function(b){
    if(state[b.id])b.checked=true;
    b.addEventListener('change',function(){state[b.id]=b.checked;save();update();});
  });
  document.querySelectorAll('.write textarea').forEach(function(ta){
    if(state[ta.id])ta.value=state[ta.id];
    ta.addEventListener('input',function(){state[ta.id]=ta.value;save();});
  });
  update();

  // プロンプトのコピー
  document.querySelectorAll('.copy').forEach(function(btn){
    btn.addEventListener('click',function(){
      var el=btn.closest('.prompt').querySelector('pre');
      function reset(t){btn.textContent=t;setTimeout(function(){btn.textContent='コピー'},1600)}
      function select(){var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r);reset('選択しました')}
      try{navigator.clipboard.writeText(el.textContent).then(function(){reset('コピーしました')},select)}catch(e){select()}
    });
  });

  // ヒアリングシート：答えを保存して、まとめてコピーする
  var hearing=document.querySelector('form.hearing');
  if(hearing){
    var hq=hearing.querySelectorAll('.hq');
    hearing.querySelectorAll('input,textarea').forEach(function(el){
      var key=el.type==='radio'?el.name:el.id;
      if(el.type==='radio'){el.checked=state[key]===el.value}else if(state[key])el.value=state[key];
      el.addEventListener(el.type==='radio'?'change':'input',function(){state[key]=el.value;save();preview();});
    });
    var pre=document.querySelector('.hearing-preview pre');
    function text(){
      var out=['【ヒアリングシート】'];
      hq.forEach(function(q){
        var r=q.querySelector('input:checked'),f=q.querySelector('textarea,input[type=text]');
        var v=(r?r.value:(f?f.value:'')).trim();
        out.push('','■'+q.dataset.q,v||'（未記入）');
      });
      return out.join('\n');
    }
    function preview(){if(pre)pre.textContent=text()}
    preview();
    var cbtn=document.querySelector('.hearing-copy'),done=document.querySelector('.hearing-done');
    cbtn.addEventListener('click',function(){
      var t=text();
      function ok(){done.hidden=false;done.textContent='コピーしました。公式LINEに貼り付けて送ってください。'}
      function ng(){var d=document.querySelector('.hearing-preview');d.open=true;var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);done.hidden=false;done.textContent='自動でコピーできなかったので、下の内容を選択しました。長押しかCtrl+Cでコピーしてください。'}
      try{navigator.clipboard.writeText(t).then(ok,ng)}catch(e){ng()}
    });
  }

  // 「ホーム画面に追加」へのリンク（#home）から来たときは、手順を開いておく
  var home=document.getElementById('home');
  if(home&&home.tagName==='DETAILS'&&location.hash==='#home') home.open=true;

  // 目次のカード：ホーム画面のアイコンから開いたとき（アプリ表示）でも、押したら必ずそのページへ移動する
  document.querySelectorAll('.cards a[href]').forEach(function(a){
    a.addEventListener('click',function(e){ if(e.metaKey||e.ctrlKey||e.shiftKey) return; e.preventDefault(); location.href=a.href; });
  });

  // 目次ページ：宿題のチェックから進み具合を出す
  var cards=document.querySelectorAll('.cards a[data-hw]');
  if(cards.length){
    var all=0,done=0,steps=0;
    cards.forEach(function(a){
      var ids=a.dataset.hw.split(' ').filter(Boolean),d=ids.filter(function(id){return state[id]}).length;
      all+=ids.length;done+=d;
      var bar=a.querySelector('.hw i');if(bar)bar.style.width=(ids.length?d/ids.length*100:0)+'%';
      if(ids.length&&d===ids.length){a.classList.add('done');steps++}
    });
    var pct=all?Math.round(done/all*100):0,m=document.querySelector('.meter');
    if(m){m.querySelector('i').style.width=pct+'%';m.setAttribute('aria-valuenow',pct)}
    var pt=document.querySelector('.progress-text');
    if(pt&&done)pt.innerHTML='<b>'+pct+'%</b>　宿題 '+done+' / '+all+'　・　完了したステップ '+steps+' / '+cards.length;
  }

  // 使い方動画：押したときだけYouTubeを読み込む
  document.querySelectorAll('.video-play').forEach(function(btn){
    btn.addEventListener('click',function(){
      var f=document.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+btn.dataset.yt+'?autoplay=1&rel=0';
      f.title=btn.getAttribute('aria-label');
      f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen=true;
      btn.replaceWith(f);
    });
  });

  // 画像を大きく表示
  var box=document.createElement('div');box.className='lightbox';box.hidden=true;
  var big=document.createElement('img');big.alt='';box.appendChild(big);document.body.appendChild(box);
  box.addEventListener('click',function(){box.hidden=true});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')box.hidden=true});
  document.querySelectorAll('.shots img,.toolshot img').forEach(function(img){
    img.addEventListener('click',function(){big.src=img.src;big.alt=img.alt;box.hidden=false});
  });
})();
