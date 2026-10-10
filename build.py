# ココナラはじめての出品ガイド：src/stepN.html の本文に共通の枠をつけて stepN.html と index.html を作る
import os, html, re, sys, shutil
D = os.path.dirname(os.path.abspath(__file__))
# python build.py        → コンサル版（ヒアリングシート・公式LINEでの質問あり）をこのフォルダに作る
# python build.py brain  → Brain版（ヒアリング・LINEサポートなし）を BRAIN_DIR に作る
BRAIN = len(sys.argv) > 1 and sys.argv[1] == 'brain'
BRAIN_DIR = 'g-vnzn5s3dc931'
OUT = os.path.join(D, BRAIN_DIR) if BRAIN else D
SRC = os.path.join(D, 'src_brain' if BRAIN else 'src')  # Brain版はツールの記載がない別原稿

def variant(h):
    # <!--consult-->…<!--/consult--> はコンサル版だけ、<!--brain-->…<!--/brain--> はBrain版だけに残す
    drop = 'consult' if BRAIN else 'brain'
    h = re.sub(r'<!--%s-->.*?<!--/%s-->\n?' % (drop, drop), '', h, flags=re.S)
    return re.sub(r'<!--/?(consult|brain)-->\n?', '', h)

TITLE = 'ココナラはじめての出品ガイド'

# (番号, 目次での名前, ページの見出し, 所要時間の目安, ゴール, 表紙での説明, 段階)
STEPS = [
 (0, 'はじめに', 'はじめに：ココナラの仕組みと準備', '約30分', 'ココナラの仕組みとお金の流れを知り、ChatGPTを使える状態にする。', 'ココナラの仕組み、ランク、お金の流れ、ChatGPTの準備、続けるための心構え', 1),
 (1, '登録と審査', '登録と審査：本人確認まで済ませる', '約20分', '会員登録・出品者情報・本人確認を終わらせ、審査で落ちやすい表現を知る。', '会員登録から本人確認まで。審査で落ちやすい3つの表現', 1),
 (2, '方向性を決める', '方向性を決める：売れているお店から学ぶ', '約40分', '売れているお店を3〜5店調べて、「私のお店は○○な人のための○○」と一文で言えるようにする。', 'モデリングと<!--consult-->競合リサーチ<!--/consult--><!--brain-->売れているお店の分析<!--/brain-->で、お店の方向性を一文にする', 1),
 (3, 'プロフィール', 'プロフィールを作る：「この人なら」と思ってもらう', '約30分', '書くべき5つの項目をそろえ、書いてはいけない情報を入れずにプロフィールを仕上げる。', '自己紹介の最初の100字、書いてはいけないこと、プロフィール画像', 1),
 (4, '商品をつくる', '商品をつくる：誰に・何を・いくらで', '約30分×2回', '悩み別の切り口で、入口・ミドル・バックの商品の出品原稿を、検索される言葉まで入れて仕上げる。', '切り口の見つけ方、最初からたくさん出品する、<!--consult-->商品づくりスタジオ<!--/consult--><!--brain-->ChatGPTで出品原稿<!--/brain-->、検索される言葉', 2),
 (5, '見た目を整える', '見た目を整える：ひと目で伝わる画像', '約40分', '6：5の商品画像を、1枚ずつ役割を決めて作る。', '画像のサイズ、1枚ずつの役割、<!--consult-->サムネイル工房<!--/consult--><!--brain-->ChatGPTで画像づくり<!--/brain-->、AIっぽさを消すコツ', 2),
 (6, '出品と取引', '出品して取引する：購入から評価まで', '約30分', '商品を公開して、最初の取引を購入から評価まで迷わず終えられるようにする。', '出品の手順、取引の流れと期限、評価の仕組み、電話・ビデオの手数料', 3),
 (7, 'ルールを守る', 'ルールを守る：財産を失わないために', '約20分', '危ないことを危険度の高い順に知り、出品前にAIで最終チェックする。', '外部誘導、実績のごまかし、言葉と画像のルール、AIでの最終チェック', 3),
 (8, '実践の準備', '実践の準備：最初の1件を迎える', '約30分', '鑑定文の良い例・よくない例と対応のしかたを知り、最初の1件を迎える準備を終える。', '鑑定文の良い例・よくない例、受注から納品までの対応、最後のチェック', 3),
 (9, 'お客様を呼ぶ', 'お客様を呼ぶ：ブログとSNS', '約40分', 'ブログやSNSで、ココナラの外からも商品ページに来てもらえる入口を作る。', '誘導は一方通行、<!--consult-->ブログジェネレーター<!--/consult--><!--brain-->ChatGPTでブログ<!--/brain-->、Threads・Instagram・TikTokライブ', 4),
 (10, '振り返って育てる', '振り返って育てる：毎月の見直しと成長', '毎月 約30分', '月に1回お店を見直して直すところを1つ決め、価格の違う商品を増やしながらお店を育てる。', '<!--consult-->お店の分析<!--/consult--><!--brain-->ChatGPTで見直し<!--/brain-->、戻るステップの選び方、商品ごとの価格、商品の入れ替え', 4),
]
PHASES = {1: ('出品の土台を作る', 'STEP 0〜3'), 2: ('売れる商品を作る', 'STEP 4〜5'), 3: ('出品して取引する', 'STEP 6〜8'), 4: ('お客様を増やして育てる', 'STEP 9〜10')}
CARD_COLORS = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']

HEAD_LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700&family=Noto+Sans+JP:wght@400;500;700&display=swap">
<link rel="stylesheet" href="guide.css?v=14">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="images/icon-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="images/icon-192.png">
<meta name="apple-mobile-web-app-title" content="出品ガイド">
<meta name="theme-color" content="#FAF6F1">
<meta name="robots" content="noindex, nofollow">'''

FOOTER = '''<footer>
  <p>手数料や規約は変わることがあります。2026年10月時点の公式ガイド・ヘルプをもとにしています。最新の内容は<a href="https://coconala.com/pages/guide_top" target="_blank" rel="noopener">ココナラ公式「ご利用ガイド」</a>で確認してください。</p>
  <p>このガイド<!--consult-->と5つのツール<!--/consult-->は虹オフィスが作ったもので、ココナラ公式のものではありません。</p>
</footer>
<script src="guide.js?v=14"></script>'''

def label_tables(h):
    def one(m):
        t = m.group(0)
        heads = re.findall(r'<th>(.*?)</th>', t)
        def row(r):
            cells = iter(heads)
            return re.sub(r'<td( class="[^"]*")?>', lambda c: f'<td{c.group(1) or ""} data-label="{next(cells, "")}">', r.group(0))
        return re.sub(r'<tr>(?:(?!</tr>).)*<td.*?</tr>', row, t, flags=re.S)
    return re.sub(r'<table>.*?</table>', one, h, flags=re.S)

def toc(current):
    links = []
    for no, short, *_ in STEPS:
        cur = ' aria-current="page"' if no == current else ''
        links.append(f'    <a href="step{no}.html"{cur}><span class="n">{no}</span><span>{short}</span></a>')
    if not BRAIN:
        cur = ' aria-current="page"' if current == 'hearing' else ''
        links.insert(0, f'    <a class="pre-link" href="hearing.html"{cur}><span class="n">✎</span><span>ヒアリング</span></a>')
    cur = ' aria-current="page"' if current == 'faq' else ''
    links.append(f'    <a class="faq-link" href="faq.html"{cur}><span class="n">?</span><span>困ったときは</span></a>')
    return '  <nav class="toc" aria-label="ステップの目次">\n    <div class="label">ステップ</div>\n' + '\n'.join(links) + '\n  </nav>'

def topbar():
    return f'<div class="topbar"><a class="brand" href="index.html"><i aria-hidden="true"></i>{TITLE}</a><span class="links"><!--consult--><a class="home" href="hearing.html">ヒアリング</a><!--/consult--><a class="home" href="faq.html">困ったときは</a><a class="home" href="index.html">目次へ</a></span></div>'

# ステップ以外のページ：(ファイル名, ページ名, 小見出し, 上の小さな文字, 目安, 前のページ, 次のページ)
EXTRA = [
 ('hearing', 'ヒアリングシート', 'はじめる前に、今の状況を教えてください', 'コンサルを始める前に', '目安：約15分',
  ('index.html', '← 目次', 'ガイドの使い方'), ('step0.html', '次へ →', 'STEP 0　はじめに')),
 ('faq', '困ったときは', 'よくある質問とつまずき解決プロンプト', 'サポート', 'どのステップからでも使えます',
  ('index.html', '← 目次', 'ガイドの使い方'), ('step0.html', 'はじめから →', 'STEP 0　はじめに')),
]

def extra_page(name, h1, sub, eyebrow, meta, prev, nxt):
    body = label_tables(open(os.path.join(SRC, f'{name}.html'), encoding='utf-8').read())
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{h1}｜{TITLE}</title>
{HEAD_LINKS}
</head>
<body>
{topbar()}
<header class="page">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{h1}<span class="sub">{sub}</span></h1>
  <div class="rainbow" aria-hidden="true"></div>
  <div class="meta"><span>{meta}</span></div>
</header>
<div class="wrap">
{toc(name)}
  <main>
{body}
<nav class="pager" aria-label="ページ移動"><a href="{prev[0]}"><span class="d">{prev[1]}</span><b>{prev[2]}</b></a><a class="next" href="{nxt[0]}"><span class="d">{nxt[1]}</span><b>{nxt[2]}</b></a></nav>
  </main>
</div>
{FOOTER}
</body>
</html>
'''

def step_page(i):
    no, short, h1, time, goal, desc, phase = STEPS[i]
    body = label_tables(open(os.path.join(SRC, f'step{no}.html'), encoding='utf-8').read())
    prev = STEPS[i-1] if i > 0 else None
    nxt = STEPS[i+1] if i < len(STEPS)-1 else None
    pager = '<nav class="pager" aria-label="前後のステップ">'
    if prev:
        pager += f'<a href="step{prev[0]}.html"><span class="d">← 前のステップ</span><b>STEP {prev[0]}　{prev[1]}</b></a>'
    else:
        pager += '<a href="index.html"><span class="d">← 目次</span><b>ガイドの使い方</b></a>'
    if nxt:
        pager += f'<a class="next" href="step{nxt[0]}.html"><span class="d">次のステップ →</span><b>STEP {nxt[0]}　{nxt[1]}</b></a>'
    else:
        pager += '<a class="next" href="index.html"><span class="d">おつかれさまでした →</span><b>目次に戻る</b></a>'
    pager += '</nav>'
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>STEP {no} {short}｜{TITLE}</title>
{HEAD_LINKS}
</head>
<body>
{topbar()}
<header class="page">
  <div class="eyebrow">STEP {no} / 10</div>
  <h1>{h1.split('：')[0]}<span class="sub">{h1.split('：')[1]}</span></h1>
  <div class="rainbow" aria-hidden="true"></div>
  <div class="meta"><span>所要時間の目安：{time}</span><span>{PHASES[phase][0]}</span></div>
</header>
<div class="wrap">
{toc(no)}
  <main>
<div class="goal"><span class="k">このステップのゴール</span><p>{goal}</p></div>
{body}
{pager}
  </main>
</div>
{FOOTER}
</body>
</html>
'''

def index_page():
    phases = []
    for p, (name, rng) in PHASES.items():
        cards = []
        for k, (no, short, h1, time, goal, desc, phase) in enumerate(STEPS):
            if phase != p: continue
            hw = ' '.join(re.findall(r'type="checkbox" id="([^"]+)"', open(os.path.join(SRC, f'step{no}.html'), encoding='utf-8').read()))
            cards.append(f'<a class="{CARD_COLORS[no % 6]}" href="step{no}.html" data-hw="{hw}"><span class="n">STEP {no}</span><b>{short}</b><span class="d">{desc}</span><span class="t">目安：{time}</span><span class="hw" aria-hidden="true"><i></i></span></a>')
        phases.append(f'<section class="phase"><h2>{name}<span>{rng}</span></h2><div class="cards">{"".join(cards)}</div></section>')
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
{HEAD_LINKS}
{topbar()}
<header class="page">
  <div class="eyebrow"><!--consult-->虹オフィス コンサル用ガイドブック<!--/consult--><!--brain-->虹オフィスのココナラ出品ガイド<!--/brain--></div>
  <h1 class="keep">ココナラ<wbr>はじめての<wbr>出品ガイド</h1>
  <div class="rainbow" aria-hidden="true"></div>
  <p class="lead">ココナラ公式ガイドで押さえるべきところと、<!--consult-->虹オフィスの5つのツール<!--/consult--><!--brain-->ChatGPTに貼るだけのプロンプト<!--/brain-->を、出品までの順番に並べました。STEP 0から順に進めれば、登録 → 方向決め → 商品づくり → 出品 → 集客 → 見直しまでたどり着けます。</p>
</header>
<div style="max-width:1120px;margin:0 auto;display:grid;gap:40px">
  <div class="card progress">
    <h3>あなたの進み具合</h3>
    <div class="meter" role="progressbar" aria-label="宿題の進み具合" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i></i></div>
    <p class="progress-text">宿題にチェックを入れると、ここに進み具合が出ます。</p>
  </div>
  <div class="card">
    <h3>このガイドの使い方</h3>
    <ul>
<!--consult-->
      <li>最初に<a href="hearing.html">ヒアリングシート</a>に答えて、虹オフィスの公式LINEに送ってください。今の状況に合わせて、どこから進めるかをご案内します。</li>
<!--/consult-->
      <li>初めての人は<a href="step0.html">STEP 0「はじめに」</a>から順に進めてください。</li>
      <li>各ステップの最後に宿題があります。チェックと記入欄の内容は、このブラウザの中だけに保存されます。</li>
      <li>画面の画像は押すと大きく表示されます。プロンプトは「コピー」を押してChatGPTに貼り付けます。</li>
      <li>出品したあとも、月に1回<a href="step10.html">STEP 10</a>でお店を見直し、必要なステップに戻って直していきます。</li>
      <li>手が止まったときは<a href="faq.html">「困ったときは」</a>を開いてください。よくある質問と、ChatGPTに貼るだけのつまずき解決プロンプトがあります。</li>
    </ul>
  </div>
  <details class="card home-add" id="home">
    <summary><b>📱 ホーム画面に置いておくと便利です</b><span>追加のしかたを見る</span></summary>
    <p>スマホのホーム画面に追加しておくと、アプリのようにワンタップで開けます。</p>
    <div class="cols2">
      <div>
        <b class="os">iPhone（Safari）</b>
        <ol class="howto">
          <li><div>Safariでこのページを開く</div></li>
          <li><div>画面下の共有ボタン（四角から矢印が出ているマーク）を押す<small>見つからないときは、右下の「…」を押してから「共有」を選びます</small></div></li>
          <li><div>メニューを下にスクロールして「ホーム画面に追加」を押す</div></li>
          <li><div>右上の「追加」を押す</div></li>
        </ol>
      </div>
      <div>
        <b class="os">Android（Chrome）</b>
        <ol class="howto">
          <li><div>Chromeでこのページを開く</div></li>
          <li><div>右上の「︙」（点が縦に3つのマーク）を押す</div></li>
          <li><div>「ホーム画面に追加」を押す</div></li>
          <li><div>「追加」を押す</div></li>
        </ol>
      </div>
    </div>
    <p class="hint">宿題のチェックや記入した内容は、開いた場所ごとに保存されます。ホーム画面に追加したら、そのあとはホーム画面のアイコンから開くようにしてください。パソコンでは、ブックマークに入れておくと便利です。</p>
  </details>
  {"".join(phases)}
<!--consult-->
  <section class="phase">
    <h2>虹オフィスの5つのツール<span>どれも無料・登録不要</span></h2>
    <div class="tools">
      <a href="https://niji-coconala-competitor-research.analia511.chatgpt.site/" target="_blank" rel="noopener"><b>競合リサーチ</b><span>STEP 2 で使う</span></a>
      <a href="https://niji-coconala-product-studio.analia511.chatgpt.site/" target="_blank" rel="noopener"><b>商品づくりスタジオ</b><span>STEP 4 で使う</span></a>
      <a href="https://coconala-thumbnail-prompt-studio.analia511.chatgpt.site/" target="_blank" rel="noopener"><b>サムネイル工房</b><span>STEP 5 で使う</span></a>
      <a href="https://niji-coconala-blog-generator.analia511.chatgpt.site/" target="_blank" rel="noopener"><b>ブログジェネレーター</b><span>STEP 9 で使う</span></a>
      <a href="https://niji-coconala-analysis.analia511.chatgpt.site/" target="_blank" rel="noopener"><b>お店の分析</b><span>STEP 10 で使う</span></a>
    </div>
  </section>
<!--/consult-->
</div>
{FOOTER}
'''

os.makedirs(OUT, exist_ok=True)
def write(name, h):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(variant(h))
write('index.html', index_page())
for e in EXTRA:
    if BRAIN and e[0] == 'hearing':
        continue
    write(f'{e[0]}.html', extra_page(*e))
for i in range(len(STEPS)):
    write(f'step{STEPS[i][0]}.html', step_page(i))
if BRAIN:
    for f in ('guide.css', 'guide.js', 'manifest.webmanifest'):
        shutil.copy(os.path.join(D, f), OUT)
    shutil.copytree(os.path.join(D, 'images'), os.path.join(OUT, 'images'), dirs_exist_ok=True)
print('built', 'Brain版' if BRAIN else 'コンサル版', OUT, len(STEPS) + 1, 'pages')
