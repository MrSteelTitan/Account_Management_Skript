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

            contact = sales_contacts.find_one({'email': contact['email']})
            contacts.append(contact['_id'])
        object['contacts'] = contacts

    if type(object['authUID']) is float:
        try:
            user = auth.create_user(email=object['email'], password='DigiScent2022!')
        except EmailAlreadyExistsError:
            user = auth.get_user_by_email(email=object['email'])


        object['authUID'] = user.uid
        print(object)

    if distributors.find_one({'email': object['email']}) is None:
        listOfNans = []
        for key in object:
            if str(object[key]).lower() == 'nan':
                listOfNans.append(key)

        for key in listOfNans:
            object.pop(key)

        distributors.insert_one(object)

    else:

        listOfKeys = ['localCollectionIds', 'useComplexFilters', 'costingPlantId', 'productionPlantIds']

        for key in listOfKeys:
            object.pop(key)

        listOfNans = []
        for key in object:
            if str(object[key]).lower() == 'nan':
                listOfNans.append(key)

        for key in listOfNans:
            object.pop(key)

        distributors.update_one({'email': object['email']},{'$set': object})

        #print(object)



print('Done!')
