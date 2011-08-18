from django.conf import settings

from ctctwspylib import CTCTConnection

class ConstantContact:
    
    LIST_GENERAL = 'http://api.constantcontact.com/ws/customers/1widget/lists/1'
    LIST_PAID = 'http://api.constantcontact.com/ws/customers/1widget/lists/2'
    
    CC_KEY = '810b6a4c-9374-46a4-a6bf-06f3549c7450'
    CC_USERNAME = '1widget'
    CC_PASSWORD = 'b3tastr33t'
    
    def __init__(self):
        self.mConnection = CTCTConnection(ConstantContact.CC_KEY, 
                                          ConstantContact.CC_USERNAME, 
                                          ConstantContact.CC_PASSWORD)
        
    def __unicode__(self):
        return self.cc_key
        
    def signup(self, email):
        params = {'email_address': email,
                  'opt_in_source': 'ACTION_BY_CONTACT',
                  'contact_lists': [self.LIST_GENERAL]                  
                  } 
        
        return self.__add_contact(params)
    
    def paid(self, email):
        params = {'email_address': email,
                  'contact_lists': [self.LIST_PAID]
                  }
        
        return self.__add_contact(params)
        
    def get_lists(self):
        return self.mConnection.get_contact_lists()
        
    def __add_contact(self, params):
        if (settings.DEBUG):
            return self.mConnection.get_xml(params)
        else:
            return self.mConnection.create_contact(params)