import time
_cache = {}
DUREE_CACHE = 300
def lire_cache(cle):
    if cle in _cache:
        valeur, timestamp = _cache[cle]
        if time.time() - timestamp < DUREE_CACHE:
            return valeur
        del _cache[cle]
    return None
def ecrire_cache(cle, valeur):
    _cache[cle] = (valeur, time.time())