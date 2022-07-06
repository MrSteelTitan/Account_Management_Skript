from firebase_admin.auth import EmailAlreadyExistsError
from firebase_admin import auth

import startup
import ut

collection, cred, accounts = startup.startup()

accounts = accounts.to_dict('records')

for object in accounts:
    object['localCollectionIds'] = str(object['localCollectionIds']).split(',')
    object = ut.unflatten(object)

    try:
        user = auth.create_user(email=object['email'], password='DigiScent2022!')
    except EmailAlreadyExistsError:
        user = auth.get_user_by_email(email=object['email'])

    object['authUID'] = user.uid

    if collection.find_one({'email': object['email']}) is None:
        collection.insert_one(object)
    else:
        collection.update_one({'email': object['email']},
                              {'$set': {'role': object['role']}})

print('Done!')
