"""Apply documented display corrections while preserving the source catalog."""
import json


def load_catalog(root):
    catalog = json.loads((root / 'catalog.json').read_text())
    overlays = ['provenance/english-alignment-v2.json', 'provenance/english-completeness-v2.json']
    changes = [change for name in overlays if (root / name).exists()
               for change in json.loads((root / name).read_text())['changes']]
    by_id = {idea['id']: idea for idea in catalog['ideas']}
    for change in changes:
        idea = by_id[change['id']]
        assert change['reason'].strip()
        allowed = {'title', 'question', 'hook', 'firstMonth', 'experiment', 'baseline',
                   'publicationPath', 'risk', 'pivot', 'resources', 'readinessReason', 'readiness'}
        assert set(change['fields']) <= allowed
        assert all(isinstance(v, str) and v.strip() for v in change['fields'].values())
        history = idea.setdefault('displayCorrection', {'reasons': [], 'previousFields': {}})
        history['reasons'].append(change['reason'])
        for key in change['fields']:
            history['previousFields'].setdefault(key, idea[key])
        idea.update(change['fields'])
    catalog['meta']['displayCorrections'] = {'overlays': overlays, 'priorText': 'displayCorrection.previousFields and unmodified catalog.json'}
    return catalog
