from firebase_admin.auth import EmailAlreadyExistsError
from firebase_admin import auth

import startup
import ut

distributors, sales_contacts, cred, accounts = startup.startup()

accounts = accounts.to_dict('records')

for object in accounts:
    object['localCollectionIds'] = str(object['localCollectionIds']).split(',')
    object['contacts'] = str(object['contacts']).split(',')
    object = ut.unflatten(object)

    if object['contacts'] is not None:
        contacts = []
        for contact in object['contacts']:
            contact = {'email': contact}
            if sales_contacts.find_one(contact) is None:
                distributor = distributors.find_one(contact)
                if distributor is not None:
                    contact['name'] = distributor['firstName'] + ' ' + distributor['lastName']
                sales_contacts.insert_one(contact)
                print(contact)

            contact = sales_contacts.find_one({'email': contact['email']})
            print(contact)
            contacts.append(contact['_id'])
        object['contacts'] = contacts

    if object['authUID'] is None:
        try:
            user = auth.create_user(email=object['email'], password='DigiScent2022!')
        except EmailAlreadyExistsError:
            user = auth.get_user_by_email(email=object['email'])

        object['authUID'] = user.uid

    if distributors.find_one({'email': object['email']}) is None:
        distributors.insert_one(object)
    else:
        distributors.update_one({'email': object['email']},
                                {'$set': {'role': object['role']}})
        distributors.update_one({'email': object['email']},
                                {'$set': {'contacts': object['contacts']}})
        distributors.update_one({'email': object['email']},
                                {'$set': {'authUID': object['authUID']}})


print('Done!')
