from django.conf import settings

def get_params():
    try:
        HASHIDS = settings.HASHIDS
    except:
        HASHIDS = {}

    salt = HASHIDS.get('SALT')
    min_length = HASHIDS.get('MIN_LENGTH')
    res = {}
    if salt: res['salt'] = salt
    if min_length: res['min_length'] = min_length

    return res

def get_regex(params):
    min_length = params.get('min_length')
    if min_length is not None:
        return f'[0-9a-zA-Z]{{{ min_length },}}'
    return '[0-9a-zA-Z]+'

PARAMS = get_params()
REGEX = get_regex(PARAMS)