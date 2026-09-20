"""Build the public GitHub Pages artifact. Python standard library only."""
import json
import hashlib
import base64
import re
from urllib.parse import urlparse
from pathlib import Path
from catalog_view import load_catalog

ROOT = Path(__file__).resolve().parents[1]
page = (ROOT / 'shell.html').read_text()
catalog = load_catalog(ROOT)
synthesis = json.loads((ROOT / 'provenance/synthesis.json').read_text())
ui = json.loads((ROOT / 'locales/ui.json').read_text())
translations = {'version':'zh-CN-v1','shared':json.loads((ROOT / 'locales/shared-zh.json').read_text()),'ideas':{}}
for batch in ['a1','a2','f1','f2']:
    data = json.loads((ROOT / f'locales/ideas-zh-{batch}.json').read_text())
    assert len(data) == 50, f'Incomplete translation batch {batch}'
    assert not (translations['ideas'].keys() & data.keys()), f'Duplicate translation IDs: {batch}'
    translations['ideas'].update(data)
scores = json.loads((ROOT / 'scores.json').read_text())
assert scores['rubric'] == json.loads((ROOT / 'rubric.json').read_text())
translations['evidence'] = {}
for batch in ['a', 'f']:
    data = json.loads((ROOT / f'locales/evidence-zh-{batch}.json').read_text())
    assert len(data) == 100
    assert not (translations['evidence'].keys() & data.keys())
    translations['evidence'].update(data)
ids = {idea['id'] for idea in catalog['ideas']}
assert len(ids) == len(catalog['ideas']) == 200
assert ids == set(translations['ideas']) == set(scores['ideas'])
assert ids == set(translations['evidence'])
assert sum(c['weight'] for c in scores['rubric']['criteria']) == 100
assert all(len(pair) == 2 and all(isinstance(x,str) and x for x in pair) for pair in ui.values())
themes = {t['id'] for t in catalog['themes']}
assert themes == set(translations['shared']['themes'])
fields = ['title','question','hook','firstMonth','experiment','baseline','publicationPath','risk','pivot','resources','readinessReason']
for idea in catalog['ideas']:
    tr = translations['ideas'][idea['id']]
    assert idea['theme'] in themes
    assert idea['readiness'] in ['start','mentor','rework']
    for field in fields:
        assert isinstance(tr[field],str) and re.search('[\u3400-\u9fff]',tr[field]), (idea['id'],field)
    assert [p['id'] for p in idea['papers']] == [p['id'] for p in tr['papers']]
    for paper in idea['papers']:
        assert urlparse(paper['url']).scheme == 'https' and urlparse(paper['url']).netloc
    score = scores['ideas'][idea['id']]
    assert set(score['evidence']) == set(translations['evidence'][idea['id']])
    for key, evidence in score['evidence'].items():
        assert evidence['field'] in set(fields) | {'papers'}, (idea['id'], key)
        assert re.search('[\u3400-\u9fff]', translations['evidence'][idea['id']][key]), (idea['id'], key)
    assert all(type(score['scores'][c['key']]) is int and 0 <= score['scores'][c['key']] <= scores['rubric']['caps'].get(c['key'],5) for c in scores['rubric']['criteria'])
    computed = sum(c['weight'] * score['scores'][c['key']] / 5 for c in scores['rubric']['criteria'])
    assert computed == score['total'], idea['id']
    assert all(score['summary'].get(l) and score['nextCheck'].get(l) for l in ['en','zh'])
catalog['meta']['status'] = 'Public student idea browser; publication authorized 2026-09-20'
catalog['meta']['historicalScorePolicy'] = catalog['meta']['scorePolicy']
catalog['meta']['scorePolicy'] = 'Original campaign scores are historical. Website sorting uses new UG200-v1 assessments, supplied separately under assessments.'
catalog['meta']['languagePolicy'] = 'Chinese beginner-facing adaptations and original English share stable IDs and common scores. Original proposals and assessments remain preserved.'

def js_data(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')

replacements = {
    '/* INLINE_STYLE */': (ROOT / 'styles.css').read_text(),
    '/* INLINE_CATALOG */': 'window.IDEA_CATALOG = ' + js_data(catalog) + ';',
    '/* INLINE_SYNTHESIS */': 'window.IDEA_SYNTHESIS = ' + js_data(synthesis) + ';',
    '/* INLINE_UI */': 'window.FIELDNOTES_UI = ' + js_data(ui) + ';',
    '/* INLINE_TRANSLATIONS */': 'window.IDEA_TRANSLATIONS = ' + js_data(translations) + ';',
    '/* INLINE_SCORES */': 'window.IDEA_SCORES = ' + js_data(scores) + ';',
    '/* INLINE_APP */': (ROOT / 'app.js').read_text(),
}
for marker, content in replacements.items():
    assert page.count(marker) == 1
    page = page.replace(marker, content)
script_hashes = ['sha256-' + base64.b64encode(hashlib.sha256(s.encode()).digest()).decode() for s in re.findall(r'<script>(.*?)</script>', page, re.S)]
csp = "default-src 'none'; script-src " + ' '.join("'" + h + "'" for h in script_hashes) + "; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"
page = page.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n  <meta http-equiv="Content-Security-Policy" content="' + csp + '">')
output = ROOT / 'docs'
output.mkdir(exist_ok=True)
(output / 'index.html').write_text(page)
(output / '.nojekyll').write_text('')
assert not re.search(r'INLINE_[A-Z]+',page)
manifest = {'version':'fieldnotes-public-v1','catalogIdeas':len(ids),'translationIdeas':len(translations['ideas']),'assessedIdeas':len(scores['ideas']),'languages':['zh-CN','en'],'indexSha256':hashlib.sha256(page.encode()).hexdigest(),'inputHashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'shell.html',ROOT/'styles.css',ROOT/'app.js',ROOT/'catalog.json',ROOT/'scores.json',ROOT/'rubric.json',ROOT/'locales/ui.json',ROOT/'locales/shared-zh.json',ROOT/'provenance/synthesis.json',ROOT/'provenance/english-alignment-v2.json',ROOT/'provenance/scoring-adjudications.json',ROOT/'scripts/build_page.py',ROOT/'scripts/catalog_view.py',ROOT/'provenance/english-completeness-v2.json',ROOT/'locales/evidence-zh-a.json',ROOT/'locales/evidence-zh-f.json',*[ROOT/f'locales/ideas-zh-{b}.json' for b in ['a1','a2','f1','f2']]]}}
(ROOT / 'provenance/build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Packaged {len(catalog["ideas"])} ideas into docs/index.html ({len(page.encode()):,} bytes)')
