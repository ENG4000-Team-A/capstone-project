import jwt

my_secret = 'my_super_secret'


def generateToken(User):
    return jwt.encode(payload=User, key=my_secret)


def validToken(accessToken):
    payload = None
    try:
        payload = jwt.decode(accessToken, key=my_secret, algorithms=['HS256', ])
    except Exception as e:
        return False, None
    return True, payload


def getUsernameFromToken(request):
    accessToken = request.headers.get('Authorization')
    isValid, payload = validToken(accessToken)
    if not isValid:
        return None
    else:
        return payload["username"]
