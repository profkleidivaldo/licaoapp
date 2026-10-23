#!/usr/bin/env python3
"""Baixa as capas das lições do site CPB mais e grava data/capas.json (+ imagens em img/)."""
import re, json, os, urllib.request
UA = {'User-Agent': 'Mozilla/5.0'}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read()
page = get('https://mais.cpb.com.br/licao-adultos/').decode('utf8', 'ignore')
cap = json.load(open('data/capas.json', encoding='utf8')) if os.path.exists('data/capas.json') else {}
os.makedirs('img', exist_ok=True)
for m in re.finditer(r'\[\{"img".*?\}\]', page):
    for it in json.loads(m.group(0)):
        t = re.match(r'Lição (\d+) - .*?\| (\d)º Trimestre (\d{4})', it['title'])
        if not t: continue
        n, q, y = t.groups(); qid = f'{y}-0{q}'
        ext = os.path.splitext(it['img'].split('?')[0])[1] or '.png'
        path = f'img/{qid}-{int(n):02d}{ext}'
        try:
            if not os.path.exists(path): open(path, 'wb').write(get(it['img']))
            src = path
        except Exception as e:
            print('imagem não baixada, usando link remoto:', e); src = it['img']
        cap.setdefault(qid, {})[str(int(n))] = {'img': src, 'periodo': it['periodo'], 'link': it['link']}
json.dump(cap, open('data/capas.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('capas.json atualizado')
