#!/usr/bin/env python3
"""Gera data/licao.json a partir do repositório Adventech/sabbath-school-lessons.

Uso:
  git clone --depth 1 https://github.com/Adventech/sabbath-school-lessons
  pip install pyyaml
  python tools/gerar_licao.py sabbath-school-lessons/src/pt/2026-04   # ou: ... src/pt auto
(O app também busca o trimestre vigente sozinho quando abre com internet.)
"""
import re, json, sys, os, yaml
Q = sys.argv[1].rstrip('/')
if len(sys.argv) > 2 and sys.argv[2] == 'auto':  # escolhe o trimestre mais recente já iniciado
    import datetime
    hoje, c = datetime.date.today(), []
    for dn in os.listdir(Q):
        if re.fullmatch(r'\d{4}-\d{2}', dn):
            ini = datetime.datetime.strptime(yaml.safe_load(open(f'{Q}/{dn}/info.yml', encoding='utf8'))['start_date'], '%d/%m/%Y').date()
            if ini <= hoje: c.append((ini, dn))
    Q = f'{Q}/{max(c)[1]}'
info = yaml.safe_load(open(Q + '/info.yml', encoding='utf8'))
weeks = []
for n in range(1, 14):
    d = f'{Q}/{n:02d}'
    if not os.path.isdir(d): break
    wi = yaml.safe_load(open(d + '/info.yml', encoding='utf8'))
    days, reads = [], ''
    for i in range(1, 8):
        raw = open(f'{d}/{i:02d}.md', encoding='utf8').read()
        fm, body = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S).groups()
        t = re.search(r'title:\s*(.*)', fm).group(1).strip().strip('"')
        body = re.sub(r'<[^>]+>', '', body.strip())
        if i == 1:
            r = re.search(r'###\s*Leituras da semana\s*\n(.*)', body)
            if r: reads, body = r.group(1).strip(), body[:r.start()].strip()
        days.append({'t': t, 'md': body})
    weeks.append({'n': n, 'title': wi['title'], 'start': wi['start_date'], 'end': wi['end_date'], 'reads': reads, 'days': days})
out = {'id': os.path.basename(Q), 'title': info['title'], 'human': info['human_date'], 'weeks': weeks}
os.makedirs('data', exist_ok=True)
json.dump(out, open('data/licao.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print('data/licao.json gerado:', len(weeks), 'semanas')
