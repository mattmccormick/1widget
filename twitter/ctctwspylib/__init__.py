'''
    Copyright 1996-2009 Constant Contact, Inc.
    
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License. 
    You may obtain a copy of the License at 
    
        http://www.apache.org/licenses/LICENSE-2.0 
        
    Unless required by applicable law or agreed to in writing, software 
    distributed under the License is distributed on an "AS IS" BASIS, 
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
    See the License for the specific language governing permissions and 
    limitations under the License. 
'''

__author__ = "Huan Lai, Constant Contact Labs"
__license__ = "http://www.apache.org/licenses/LICENSE-2.0"

from restful_lib import Connection
from urllib import quote, quote_plus, urlencode
import xml.etree.ElementTree as ET
import re

class InvalidUsernameException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
            
"""
    -CTCTConnection-
    
    Python library class using REST to communicate with the Constant Contact Web Service API.
"""
class CTCTConnection:
    API_BASE_URL = "https://api.constantcontact.com/ws/customers/"
    DO_NOT_INCLUDE_LISTS = ['Removed', 'Do Not Mail', 'Active']
    
    EVENTS_BOUNCES = 0
    EVENTS_CLICKS = 1
    EVENTS_FORWARDS = 2
    EVENTS_OPENS = 3
    EVENTS_OPT_OUTS = 4
    EVENTS_SENDS = 5
	
    CAMPAIGNS_ALL = 0
    CAMPAIGNS_DRAFT = 1
    CAMPAIGNS_RUNNING = 2
    CAMPAIGNS_SENT = 3
    CAMPAIGNS_SCHEDULED = 4
    
    #atom namespace
    NS_ATOM = 'http://www.w3.org/2005/Atom'
    
    #constantcontact namespace
    NS_CTCT = 'http://ws.constantcontact.com/ns/1.0/'
    
    def __init__(self, api_key, username, password):
        self.username = username 
        login_username = api_key + "%" + username
        
        connection_base = CTCTConnection.API_BASE_URL + username + "/"
        
        self.connection = Connection(connection_base, username=login_username, password=password)

    def verify_credentials(self):
        """ Returns whether or not the apikey, username and password the object was initialized are valid """
        response = self.connection.request_get("/")

        # Web service returns a 200 status code if successful
        if(int(response['headers']['status']) == 200):
            return True                                  #valid username, valid credentials
        else:
            if re.match('^[\w.@-]{6,}$', self.username): #does username only contain allowable characters? valid are a-zA-Z0-9.-_@
                return False                             #valid username, invalid credentials
            else:
                raise InvalidUsernameException('This user name contains characters that are no '
                                               'longer supported. Please log in to '
                                               'constantcontact.com and update your user name.')
        
    def get_contact_lists(self, path=None):
        """ Returns all of the Contact Lists from ConstantContact. 
            No parameters are necessary """
        contact_lists = []
        
        # Default path
        if(path == None):
            path = '/lists'
            
        response = self.connection.request_get(path)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        # Check if there is a next link
        links = xml.findall('{http://www.w3.org/2005/Atom}link');
        next_path = None
        for link in links:
            if(link.get('rel') == 'next'):
                next_link = link.get('href')
                slash = next_link.find('/lists')
                next_path = next_link[slash:]
                break
        
        # Get all of the contact lists
        entries = xml.findall('{http://www.w3.org/2005/Atom}entry')
        for entry in entries:
            contact_list = {'id': entry.findtext('{http://www.w3.org/2005/Atom}id'),
                            'name': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                   '{http://ws.constantcontact.com/ns/1.0/}ContactList/'
                                                   '{http://ws.constantcontact.com/ns/1.0/}Name'),
                            'updated': entry.findtext('{http://www.w3.org/2005/Atom}updated')}
            
            # Don't include some lists
            if(contact_list['name'] not in CTCTConnection.DO_NOT_INCLUDE_LISTS):
                contact_lists.append(contact_list)
            
        # If there is a next link, recursively retrieve from there too
        if(next_path != None):
            contact_lists.extend(self.get_contact_lists(path=next_path))
            
        return contact_lists
    
    def get_contact_list(self, list_id_number):
        """ Returns detailed information about an individual Contact List 
            Requires the contact list id number """
        contact_list_id = '/lists/' + str(list_id_number)
        response = self.connection.request_get(contact_list_id)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        contact_list_xml = xml.find('{http://www.w3.org/2005/Atom}content/'
                                    '{http://ws.constantcontact.com/ns/1.0/}ContactList')
        
        list = {'id': xml.findtext('{http://www.w3.org/2005/Atom}id'),
                    'updated': xml.findtext('{http://www.w3.org/2005/Atom}updated'),
                    'name': contact_list_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Name'),
                    'opt_in_default': contact_list_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}OptInDefault'),
                    'short_name': contact_list_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}ShortName'),
                    'sort_order': contact_list_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}SortOrder')
                   }
        
        return list
		
    def get_contact_list_members(self, list_id_number=None, path=None):
        """ Returns all of the Contacts in a Contact List 
            list_id_number parameter is required """
        contacts = []
        
        # Default path
        if(path == None):
            path = "lists/" + str(list_id_number) + "/members"
            
        response = self.connection.request_get(path)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        # Check if there is a next link
        links = xml.findall('{http://www.w3.org/2005/Atom}link');
        next_path = None
        for link in links:
            if(link.get('rel') == 'next'):
                next_link = link.get('href')
                slash = next_link.find('/lists')
                next_path = next_link[slash:]
                break
            
        # Get all of the contacts
        entries = xml.findall('{http://www.w3.org/2005/Atom}entry')
        for entry in entries:
            contact = {'id': entry.findtext('{http://www.w3.org/2005/Atom}id'),
                       'name': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                              '{http://ws.constantcontact.com/ns/1.0/}ContactListMember/'
                                              '{http://ws.constantcontact.com/ns/1.0/}Name'),
                       'email_address': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                       '{http://ws.constantcontact.com/ns/1.0/}ContactListMember/'
                                                       '{http://ws.constantcontact.com/ns/1.0/}EmailAddress'),
                       'updated': entry.findtext('{http://www.w3.org/2005/Atom}updated')}
            
            contacts.append(contact)
            
        # If there is a next link, recursively retrieve from there too
        if(next_path != None):
            contacts.extend(self.get_contact_list_members(path=next_path))
            
        return contacts
    
    def create_contact_list(self, contact_list_name):
        """ Creates a new contact list. Returns true if successful """
        body = """
            <entry xmlns="http://www.w3.org/2005/Atom">
                <id>data:,</id>
                <title/>
                <author/>
                <updated>2008-04-16</updated>
                <content type="application/vnd.ctct+xml">
                    <ContactList xmlns="http://ws.constantcontact.com/ns/1.0/">
                        <OptInDefault>false</OptInDefault>
                        <Name>""" + str(contact_list_name) + """</Name>
                        <SortOrder>99</SortOrder>
                    </ContactList>
                </content>
            </entry>
        """
        response = self.connection.request_post('/lists', body=body, headers={'Content-Type': 'application/atom+xml'})
        
        # Web service returns 201 status code if successful
        if(int(response['headers']['status']) == 201):
            return True
        else:
            return False
            
    def update_contact_list(self, params, list_id_number):
        """ Updates an existing Contact List to the ConstantContact server. 
            Takes in a dictionary of parameters
            list_id_number parameter is required
            """
        contact_list_uri = '/lists/' + str(list_id_number)
        response = self.connection.request_get(contact_list_uri)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        contact_list_xml = xml.find('{http://www.w3.org/2005/Atom}content')
        
        if('name' not in params):
            params['name'] = contact_list_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}ContactList/'
                                                       '{http://ws.constantcontact.com/ns/1.0/}Name')
        if('opt_in_default' not in params):
            params['opt_in_default'] = contact_list_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}ContactList/'
                                                                 '{http://ws.constantcontact.com/ns/1.0/}OptInDefault')
        if('sort_order' not in params):
            params['sort_order'] = contact_list_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}ContactList/'
                                                             '{http://ws.constantcontact.com/ns/1.0/}SortOrder')

        xml_update_body = """
                <content type="application/vnd.ctct+xml" xmlns="http://www.w3.org/2005/Atom">
                    <ContactList xmlns="http://ws.constantcontact.com/ns/1.0/">
                        <Name>""" + params['name'] + """</Name>
                        <OptInDefault>""" + params['opt_in_default'] + """</OptInDefault>
                        <SortOrder>""" + params['sort_order'] + """</SortOrder>
                    </ContactList>
                </content>
        """
        
        xml.remove(contact_list_xml)
        xml.append(ET.fromstring(xml_update_body))
        
        response = self.connection.request_put(contact_list_uri, body=ET.tostring(xml), headers={'Content-Type': 'application/atom+xml'})
        
        #Web service returns 201 or 204 status code if successful
        if(int(response['headers']['status']) == 201 or int(response['headers']['status']) == 204):
            return True
        else:
            return False
            
    def delete_contact_list(self, list_id_number):
        """ Deletes an existing contact list. Returns true if successful """
        list_uri = '/lists/' + str(list_id_number)
        response = self.connection.request_delete(list_uri)
        
        # Web service returns 204 status code if successful
        if(int(response['headers']['status']) == 204):
            return True
        else:
            return False
        
    def get_contacts(self, email=None, path=None):
        """ Returns all of the Contacts from ConstantContact. 
            If an email address is given, only return the Contact with that email address """
        contacts = []
        
        # ConstantContact web services provides for a way to search for an exact match email address
        if(email != None):
            path = '/contacts?email=' + email
        # Default path
        elif(path == None):
            path = '/contacts'
            
        response = self.connection.request_get(path)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        # Check if there is a next link
        links = xml.findall('{http://www.w3.org/2005/Atom}link');
        next_path = None
        for link in links:
            if(link.get('rel') == 'next'):
                next_link = link.get('href')
                slash = next_link.find('/contacts')
                next_path = next_link[slash:]
                break
            
        # Get all of the contacts
        entries = xml.findall('{http://www.w3.org/2005/Atom}entry')
        for entry in entries:
            contact = {'id': entry.findtext('{http://www.w3.org/2005/Atom}id'),
                       'status': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                '{http://ws.constantcontact.com/ns/1.0/}Contact/'
                                                '{http://ws.constantcontact.com/ns/1.0/}Status'),
                       'email_address': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                       '{http://ws.constantcontact.com/ns/1.0/}Contact/'
                                                       '{http://ws.constantcontact.com/ns/1.0/}EmailAddress'),
                       'email_type': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                    '{http://ws.constantcontact.com/ns/1.0/}Contact/'
                                                    '{http://ws.constantcontact.com/ns/1.0/}EmailType'),
                       'name': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                              '{http://ws.constantcontact.com/ns/1.0/}Contact/'
                                              '{http://ws.constantcontact.com/ns/1.0/}Name'),
                       'opt_in_time': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                     '{http://ws.constantcontact.com/ns/1.0/}Contact/'
                                                     '{http://ws.constantcontact.com/ns/1.0/}OptInTime'),
                       'opt_in_source': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                       '{http://ws.constantcontact.com/ns/1.0/}Contact/'
                                                       '{http://ws.constantcontact.com/ns/1.0/}OptInSource'),
                       'updated': entry.findtext('{http://www.w3.org/2005/Atom}updated')}
            
            contacts.append(contact)
            
        # If there is a next link, recursively retrieve from there too
        if(next_path != None):
            contacts.extend(self.get_contacts(path=next_path))
            
        return contacts
        
    def query_contacts(self, emails, path=None):
        """ Queries a list of contacts and returns only matching contacts """
        contacts = []
        
        #get the namespaces for use locally
        atom = CTCTConnection.NS_ATOM
        ctct = CTCTConnection.NS_CTCT
        
        if(path==None):
            path = '/contacts?'
            for email in emails:
                path += urlencode({'email':email}) + '&' #trailing ampersand won't hurt
        
        response = self.connection.request_get(path)
        
        if(int(response['headers']['status']) != 200):
            return None
            
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        # Check if there is a next link
        links = xml.findall('{%s}link' % (atom));
        next_path = None
        for link in links:
            if(link.get('rel') == 'next'):
                next_link = link.get('href')
                slash = next_link.find('/contacts')
                next_path = next_link[slash:]
                break
        
        # Get all of the contacts that were found
        entries = xml.findall('{%s}entry' % (atom))
        for entry in entries:
            contact = {'id': entry.findtext('{%s}id' % (atom)),
                       'status': entry.findtext('{%s}content/{%s}Contact/{%s}Status' % (atom, ctct, ctct)),
                       'email_address': entry.findtext('{%s}content/{%s}Contact/{%s}EmailAddress' % (atom, ctct, ctct)),
                       'email_type': entry.findtext('{%s}content/{%s}Contact/{%s}EmailType' % (atom, ctct, ctct)),
                       'name': entry.findtext('{%s}content/{%s}Contact/{%s}Name' % (atom, ctct, ctct)),
                       'opt_in_time': entry.findtext('{%s}content/{%s}Contact/{%s}OptInTime' % (atom, ctct, ctct)),
                       'opt_in_source': entry.findtext('{%s}content/{%s}Contact/{%s}OptInSource' % (atom, ctct, ctct)),
                       'updated': entry.findtext('{%s}updated' % (atom))}
            
            contacts.append(contact)
            
        # If there is a next link, recursively retrieve from there too
        if(next_path != None):
            contacts.extend(self.query_contacts(path=next_path))
        
        return contacts
    
    def get_contact(self, email=None, contact_id_number=None):
        """ Returns detailed information about an individual Contact 
            Either email or contact id number required 
            If both are given, use the contact_id_number, as it requires less work on our part """

        if(contact_id_number):
            contact_uri = "/contacts/" + str(contact_id_number)
        else:
            contacts = self.get_contacts(email=email)
            if(not contacts):
                return None
            
            contact_uri = contacts[0]['id']
            contact_uri = "/contacts" + contact_uri[contact_uri.rindex("/"):]
        
        response = self.connection.request_get(contact_uri)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        contact_xml = xml.find('{http://www.w3.org/2005/Atom}content/'
                               '{http://ws.constantcontact.com/ns/1.0/}Contact')
        
        # Get all of the Contact Lists this Contact is subscribed to
        contact_lists = []
        contact_lists_xml = contact_xml.findall('{http://ws.constantcontact.com/ns/1.0/}ContactLists/'
                                                '{http://ws.constantcontact.com/ns/1.0/}ContactList')
        for contact_list in contact_lists_xml:
            contact_lists.append(contact_list.get('id'))
        
        contact = {'id': xml.findtext('{http://www.w3.org/2005/Atom}id'),
                   'updated': xml.findtext('{http://www.w3.org/2005/Atom}updated'),
                   'status': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Status'),
                   'email_address': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}EmailAddress'),
                   'email_type': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}EmailType'),
                   'name': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Name'),
                   'first_name': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}FirstName'),
                   'middle_name': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}MiddleName'),
                   'last_name': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}LastName'),
                   'job_title': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}JobTitle'),
                   'company_name': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CompanyName'),
                   'home_phone': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}HomePhone'),
                   'work_phone': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}WorkPhone'),
                   'addr1': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Addr1'),
                   'addr2': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Addr2'),
                   'addr3': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Addr3'),
                   'city': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}City'),
                   'state_code': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}StateCode'),
                   'state_name': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}StateName'),
                   'country_code': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CountryCode'),
                   'country_name': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CountryName'),
                   'postal_code': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}PostalCode'),
                   'sub_postal_code': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}SubPostalCode'),
                   'note': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Note'),
                   'custom_field1': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField1'),
                   'custom_field2': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField2'),
                   'custom_field3': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField3'),
                   'custom_field4': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField4'),
                   'custom_field5': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField5'),
                   'custom_field6': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField6'),
                   'custom_field7': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField7'),
                   'custom_field8': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField8'),
                   'custom_field9': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField9'),
                   'custom_field10': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField10'),
                   'custom_field11': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField11'),
                   'custom_field12': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField12'),
                   'custom_field13': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField13'),
                   'custom_field14': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField14'),
                   'custom_field15': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}CustomField15'),
                   'contact_lists': contact_lists,
                   'confirmed': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Confirmed'),
                   'insert_time': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}InsertTime'),
                   'last_update_time': contact_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}LastUpdateTime'),
                   }
        
        return contact
    
    def get_xml(self, params):
        return self.__create_contact_xml(params)
    
    def create_contact(self, params):
        """ Adds a new Contact to the ConstantContact server. 
            Takes in a dictionary of parameters """
        xml_body = self.__create_contact_xml(params)
        response = self.connection.request_post('/contacts', body=xml_body, headers={'Content-Type': 'application/atom+xml'})
        
        # Web service returns 201 status code if successful
        if(int(response['headers']['status']) == 201):
            return True
        else:
            return False
        
    def update_contact(self, params, email=None, contact_id_number=None):
        """ Updates an existing Contact to the ConstantContact server. 
            Takes in a dictionary of parameters
            Either email or contact id number required 
                If both are given, use the contact_id_number, as it requires less work on our part """
        if(contact_id_number):
            contact_uri = "/contacts/" + str(contact_id_number)
        else:
            contacts = self.get_contacts(email=email)
            if(not contacts):
                return None
            
            contact_uri = contacts[0]['id']
            contact_uri = "/contacts" + contact_uri[contact_uri.rindex("/"):]
            
            
        xml_body = self.__create_contact_xml(params)
        response = self.connection.request_put(contact_uri, body=xml_body, headers={'Content-Type': 'application/atom+xml'})
        
        # Web service returns 201 or 204 status code if successful
        if(int(response['headers']['status']) == 201 or int(response['headers']['status']) == 204):
            return True
        else:
            return False
    
    def delete_contact(self,  email=None, contact_id_number=None):
        """ Modifies a contact to DO_NOT_MAIL. Returns true if successful
            Either email or contact id number required 
            If both are given, use the contact_id_number, as it requires less work on our part """
        if(contact_id_number):
            contact_uri = "/contacts/" + str(contact_id_number)
        else:
            contacts = self.get_contacts(email=email)
            if(not contacts):
                return None
            
            contact_uri = contacts[0]['id']
            contact_uri = "/contacts" + contact_uri[contact_uri.rindex("/"):]
        
        response = self.connection.request_delete(contact_uri)
        
        # Web service returns 204 status code if successful
        if(int(response['headers']['status']) == 204):
            return True
        else:
            return False
    
    def __create_contact_xml(self, params):
        """ Generates a valid XML string from user given parameters to be sent to 
        ConstantContact web services """
        contact_lists_array = []
        for list in params['contact_lists']:
            contact_lists_array.append('<ContactList id="' + list + '" />')
            
        contact_lists = ''.join(contact_lists_array)
        
        xml_body = """
            <entry xmlns="http://www.w3.org/2005/Atom">
                <title type="text"></title>
                <updated>2008-07-23T14:21:06.407Z</updated>
                <author></author>
                <id>%s</id>
                <summary type="text">Contact</summary>
                <content type="application/vnd.ctct+xml">
                    <Contact xmlns="http://ws.constantcontact.com/ns/1.0/">
                        <Status>%s</Status>
                        <EmailAddress>%s</EmailAddress>
                        <EmailType>%s</EmailType>
                        <FirstName>%s</FirstName>
                        <MiddleName>%s</MiddleName>
                        <LastName>%s</LastName>
                        <JobTitle>%s</JobTitle>
                        <CompanyName>%s</CompanyName>
                        <HomePhone>%s</HomePhone>
                        <WorkPhone>%s</WorkPhone>
                        <Addr1>%s</Addr1>
                        <Addr2>%s</Addr2>
                        <Addr3>%s</Addr3>
                        <City>%s</City>
                        <StateCode>%s</StateCode>
                        <StateName>%s</StateName>
                        <CountryCode>%s</CountryCode>
                        <CountryName>%s</CountryName>
                        <PostalCode>%s</PostalCode>
                        <SubPostalCode>%s</SubPostalCode>
                        <Note>%s</Note>
                        <CustomField1>%s</CustomField1>
                        <CustomField2>%s</CustomField2>
                        <CustomField3>%s</CustomField3>
                        <CustomField4>%s</CustomField4>
                        <CustomField5>%s</CustomField5>
                        <CustomField6>%s</CustomField6>
                        <CustomField7>%s</CustomField7>
                        <CustomField8>%s</CustomField8>
                        <CustomField9>%s</CustomField9>
                        <CustomField10>%s</CustomField10>
                        <CustomField11>%s</CustomField11>
                        <CustomField12>%s</CustomField12>
                        <CustomField13>%s</CustomField13>
                        <CustomField14>%s</CustomField14>
                        <CustomField15>%s</CustomField15>

                        <OptInSource>%s</OptInSource>
                        
                        <ContactLists>
                            %s
                        </ContactLists>
                    </Contact>
                </content>
            </entry>
        """ % (params['id'] if 'id' in params else 'data:,none', 
               params['status'] if 'status' in params else '', 
               params['email_address'] if 'email_address' in params else '', 
               params['email_type'] if 'email_type' in params else '', 
               params['first_name'] if 'first_name' in params else '', 
               params['middle_name'] if 'middle_name' in params else '', 
               params['last_name'] if 'last_name' in params else '', 
               params['job_title'] if 'job_title' in params else '', 
               params['company_name'] if 'company_name' in params else '', 
               params['home_phone'] if 'home_phone' in params else '', 
               params['work_phone'] if 'work_phone' in params else '', 
               params['addr1'] if 'addr1' in params else '', 
               params['addr2'] if 'addr2' in params else '', 
               params['addr3'] if 'addr3' in params else '', 
               params['city'] if 'city' in params else '', 
               params['state_code'] if 'state_code' in params else '', 
               params['state_name'] if 'state_name' in params else '', 
               params['country_code'] if 'country_code' in params else '', 
               params['country_name'] if 'country_name' in params else '', 
               params['postal_code'] if 'postal_code' in params else '', 
               params['sub_postal_code'] if 'sub_postal_code' in params else '', 
               params['note'] if 'note' in params else '', 
               params['custom_field1'] if 'custom_field1' in params else '', 
               params['custom_field2'] if 'custom_field2' in params else '', 
               params['custom_field3'] if 'custom_field3' in params else '', 
               params['custom_field4'] if 'custom_field4' in params else '', 
               params['custom_field5'] if 'custom_field5' in params else '',
               params['custom_field6'] if 'custom_field6' in params else '', 
               params['custom_field7'] if 'custom_field7' in params else '', 
               params['custom_field8'] if 'custom_field8' in params else '', 
               params['custom_field9'] if 'custom_field9' in params else '',
               params['custom_field10'] if 'custom_field10' in params else '', 
               params['custom_field11'] if 'custom_field11' in params else '', 
               params['custom_field12'] if 'custom_field12' in params else '', 
               params['custom_field13'] if 'custom_field13' in params else '',
               params['custom_field14'] if 'custom_field14' in params else '', 
               params['custom_field15'] if 'custom_field15' in params else '', 
               params['opt_in_source'] if 'opt_in_source' in params else 'ACTION_BY_CUSTOMER', 
               contact_lists)
        
        return xml_body
    
    def get_contact_events(self, event_type, email=None, contact_id_number=None, path=None):
        """ Returns events associated with a Contact (within the past 90 days) 
        based on the given event type event_type is one of (EVENTS_BOUNCES, 
        EVENTS_CLICKS, EVENTS_FORWARDS, EVENTS_OPENS, EVENTS_OUT_OUTS, EVENTS_SENDS) """
        events = []
            
        # Get the contact_id_number from the email address if the user didn't provide one
        if(not contact_id_number):
            contacts = self.get_contacts(email=email)
            if(not contacts):
                return None
            
            contact_id = contacts[0]["id"]
            contact_id_number = contact_id[contact_id.rindex("/")+1:]
        
        if(event_type == self.EVENTS_BOUNCES):
            request_string = '/contacts/' + str(contact_id_number) + '/events/bounces'
            event_string = 'BounceEvent'
        elif(event_type == self.EVENTS_CLICKS):
            request_string = '/contacts/' + str(contact_id_number) + '/events/clicks'
            event_string = 'ClickEvent'
        elif(event_type == self.EVENTS_FORWARDS):
            request_string = '/contacts/' + str(contact_id_number) + '/events/forwards'
            event_string = 'ForwardEvent'
        elif(event_type == self.EVENTS_OPENS):
            request_string = '/contacts/' + str(contact_id_number) + '/events/opens'
            event_string = 'OpenEvent'
        elif(event_type == self.EVENTS_OPT_OUTS):
            request_string = '/contacts/' + str(contact_id_number) + '/events/optouts'
            event_string = 'OptOutEvent'
        elif(event_type == self.EVENTS_SENDS):
            request_string = '/contacts/' + str(contact_id_number) + '/events/sends'
            event_string = 'SentEvent'
        else:
            return None
        
        if(path):
            request_string = path
        
        response = self.connection.request_get(request_string)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        # Check if there is a next link
        links = xml.findall('{http://www.w3.org/2005/Atom}link');
        next_path = None
        for link in links:
            if(link.get('rel') == 'next'):
                next_link = link.get('href')
                slash = next_link.find('/contacts')
                next_path = next_link[slash:]
                break
        
        # Get all of the contact lists
        entries = xml.findall('{http://www.w3.org/2005/Atom}entry')
        for entry in entries:
            contact = entry.find('{http://www.w3.org/2005/Atom}content/{http://ws.constantcontact.com/ns/1.0/}' +
                                 event_string +
                                 '/{http://ws.constantcontact.com/ns/1.0/}Contact')
            campaign = entry.find('{http://www.w3.org/2005/Atom}content/{http://ws.constantcontact.com/ns/1.0/}' +
                                  event_string +
                                  '/{http://ws.constantcontact.com/ns/1.0/}Campaign')

            event = {'id': entry.findtext('{http://www.w3.org/2005/Atom}id'),
                     'updated': entry.findtext('{http://www.w3.org/2005/Atom}updated'),
                     'event_time': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                  '{http://ws.constantcontact.com/ns/1.0/}' + event_string + '/'
                                                  '{http://ws.constantcontact.com/ns/1.0/}EventTime'),
                     'contact_id': contact.get('id'),
                     'contact_email_address': contact.findtext('{http://ws.constantcontact.com/ns/1.0/}EmailAddress'),
                     'campaign': campaign.get('id')
                     }
            if(event_type == self.EVENTS_CLICKS):
                event['link_url'] = entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                   '{http://ws.constantcontact.com/ns/1.0/}' + event_string +
                                                   '/{http://ws.constantcontact.com/ns/1.0/}LinkUrl'),
                      
            events.append(event)
                     
        # If there is a next link, recursively retrieve from there too
        if(next_path != None):
            events.extend(self.get_campaigns(contact_id_number=contact_id_number, event_type=event_type, path=next_path))
            
        return events                   
    
    def get_campaigns(self, type=CAMPAIGNS_ALL, path=None):
        """ Returns all of the Campaigns from ConstantContact. """
        campaigns = []
        
        # Default path
        if(path == None):
			if(type == self.CAMPAIGNS_DRAFT):
				path = '/campaigns?status=DRAFT'
			elif(type == self.CAMPAIGNS_RUNNING):
				path = '/campaigns?status=RUNNING'
			elif(type == self.CAMPAIGNS_SENT):
				path = '/campaigns?status=SENT'
			elif(type == self.CAMPAIGNS_SCHEDULED):
				path = '/campaigns?status=SCHEDULED'
			else:
				path = '/campaigns'
            
        response = self.connection.request_get(path)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        # Check if there is a next link
        links = xml.findall('{http://www.w3.org/2005/Atom}link');
        next_path = None
        for link in links:
            if(link.get('rel') == 'next'):
                next_link = link.get('href')
                slash = next_link.find('/campaigns')
                next_path = next_link[slash:]
                break
        
        # Get all of the campaigns
        entries = xml.findall('{http://www.w3.org/2005/Atom}entry')
        for entry in entries:
            campaign = {'id': entry.findtext('{http://www.w3.org/2005/Atom}id'),
                        'name': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                               '{http://ws.constantcontact.com/ns/1.0/}Campaign/'
                                               '{http://ws.constantcontact.com/ns/1.0/}Name'),
                        'status': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                 '{http://ws.constantcontact.com/ns/1.0/}Campaign/'
                                                 '{http://ws.constantcontact.com/ns/1.0/}Status'),
                        'date': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                               '{http://ws.constantcontact.com/ns/1.0/}Campaign/'
                                               '{http://ws.constantcontact.com/ns/1.0/}Date'),
                        'updated': entry.findtext('{http://www.w3.org/2005/Atom}updated')}
            
            campaigns.append(campaign)
            
        # If there is a next link, recursively retrieve from there too
        if(next_path != None):
            campaigns.extend(self.get_campaigns(next_path))
            
        return campaigns
    
    def get_campaign(self, campaign_id_number):
        """ Returns detailed information about an individual Campaign 
            Requires the campaign id number """
        campaign_id = '/campaigns/' + str(campaign_id_number)
        response = self.connection.request_get(campaign_id)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        campaign_xml = xml.find('{http://www.w3.org/2005/Atom}content/'
                                '{http://ws.constantcontact.com/ns/1.0/}Campaign')
        
        # Get all of the Contact Lists this Campaign was sent to
        contact_lists = []
        contact_lists_xml = campaign_xml.findall('{http://ws.constantcontact.com/ns/1.0/}ContactLists/'
                                                 '{http://ws.constantcontact.com/ns/1.0/}ContactList')
        for contact_list in contact_lists_xml:
            contact_lists.append({'id': contact_list.get('id')})
            
        # Get all of the urls
        urls = []
        urls_xml = campaign_xml.findall('{http://ws.constantcontact.com/ns/1.0/}Urls/'
                                        '{http://ws.constantcontact.com/ns/1.0/}Url')
        for url in urls_xml:
            urls.append({'id': url.get('id'),
                         'value': url.findtext('{http://ws.constantcontact.com/ns/1.0/}Value'),
                         'clicks': url.findtext('{http://ws.constantcontact.com/ns/1.0/}Clicks')
                         })
        
        campaign = {'id': xml.findtext('{http://www.w3.org/2005/Atom}id'),
                    'updated': xml.findtext('{http://www.w3.org/2005/Atom}updated'),
                    'status': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Status'),
                    'name': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Name'),
                    'date': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Date'),
                    'last_edit_date': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}LastEditDate'),
                    'last_run_date': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}LastRunDate'),
                    'sent': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Sent'),
                    'opens': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Opens'),
                    'clicks': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Clicks'),
                    'bounces': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Bounces'),
                    'forwards': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}Forwards'),
                    'opt_outs': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}OptOuts'),
                    'spam_reports': campaign_xml.findtext('{http://ws.constantcontact.com/ns/1.0/}SpamReports'),
                    'contact_lists': contact_lists,
                    'urls': urls
                   }
        
        return campaign

    def get_campaign_events(self, campaign_id_number, event_type, path=None):
        """ Returns events associated with a Contact (within the past 90 days) 
        based on the given event type event_type is one of CTCTConnection.{EVENTS_BOUNCES, 
        EVENTS_CLICKS, EVENTS_FORWARDS, EVENTS_OPENS, EVENTS_OUT_OUTS, EVENTS_SENDS} """
        events = []
        
        if(event_type == self.EVENTS_BOUNCES):
            request_string = '/campaigns/' + str(campaign_id_number) + '/events/bounces'
            event_string = 'BounceEvent'
        elif(event_type == self.EVENTS_FORWARDS):
            request_string = '/campaigns/' + str(campaign_id_number) + '/events/forwards'
            event_string = 'ForwardEvent'
        elif(event_type == self.EVENTS_OPENS):
            request_string = '/campaigns/' + str(campaign_id_number) + '/events/opens'
            event_string = 'OpenEvent'
        elif(event_type == self.EVENTS_OPT_OUTS):
            request_string = '/campaigns/' + str(campaign_id_number) + '/events/optouts'
            event_string = 'OptOutEvent'
        elif(event_type == self.EVENTS_SENDS):
            request_string = '/campaigns/' + str(campaign_id_number) + '/events/sends'
            event_string = 'SentEvent'
        elif(event_type == self.EVENTS_CLICKS):
            return self.__get_campaign_events_clicks(campaign_id_number)
        else:
            return None
        
        if(path):
            request_string=path
        
        response = self.connection.request_get(request_string)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        # Check if there is a next link
        links = xml.findall('{http://www.w3.org/2005/Atom}link');
        next_path = None
        for link in links:
            if(link.get('rel') == 'next'):
                next_link = link.get('href')
                slash = next_link.find('/campaigns')
                next_path = next_link[slash:]
                break
        
        # Get all of the contact lists
        entries = xml.findall('{http://www.w3.org/2005/Atom}entry')
        for entry in entries:
            contact = entry.find('{http://www.w3.org/2005/Atom}content/'
                                 '{http://ws.constantcontact.com/ns/1.0/}' + event_string +
                                 '/{http://ws.constantcontact.com/ns/1.0/}Contact')
            campaign = entry.find('{http://www.w3.org/2005/Atom}content/'
                                  '{http://ws.constantcontact.com/ns/1.0/}' + event_string +
                                  '/{http://ws.constantcontact.com/ns/1.0/}Campaign')
            event = {'id': entry.findtext('{http://www.w3.org/2005/Atom}id'),
                     'updated': entry.findtext('{http://www.w3.org/2005/Atom}updated'),
                     'event_time': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                  '{http://ws.constantcontact.com/ns/1.0/}' + event_string +
                                                  '/{http://ws.constantcontact.com/ns/1.0/}EventTime'),
                     'contact_id': contact.get('id'),
                     'contact_email_address': contact.findtext('{http://ws.constantcontact.com/ns/1.0/}EmailAddress'),
                     'campaign': campaign.get('id')
                     }        
                     
            events.append(event)
                     
        # If there is a next link, recursively retrieve from there too
        if(next_path != None):
            events.extend(self.get_campaign_events(campaign_id_number, event_type, path=next_path))
            
        return events  
        
    def __get_campaign_events_clicks(self, campaign_id_number, path=None):
        """ Campaign Click Events are organized differently by the ConstantContact web services than other Campaign Events 
            Returns all click events for a campaign as well as details about each url """
        urls = []
        campaign = self.get_campaign(campaign_id_number)
        
        # If the campaign doesn't exist, return None
        if(not campaign):
            return None
        
        # Loop through all of the urls, getting all of the click events for each one
        for campaign_url in campaign['urls']:
            request_string = campaign_url['id']
            slash = request_string.find('/campaigns')
            request_string = request_string[slash:]
            
            events = self.__get_campaign_events_click_single_url(request_string)
            urls.append({'events': events,
                         'id': campaign_url['id'],
                         'value': campaign_url['value'],
                         'clicks': campaign_url['clicks']
                         })
            
        return urls
            
    def __get_campaign_events_click_single_url(self, path):
        """ Returns all click events for a single url for a single campaign """
        events = []
        
        response = self.connection.request_get(path)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        
        # Check if there is a next link
        links = xml.findall('{http://www.w3.org/2005/Atom}link');
        next_path = None
        for link in links:
            if(link.get('rel') == 'next'):
                next_link = link.get('href')
                slash = next_link.find('/campaigns')
                next_path = next_link[slash:]
                break
        
        # Get all of the contact lists
        entries = xml.findall('{http://www.w3.org/2005/Atom}entry')
        for entry in entries:
            contact = entry.find('{http://www.w3.org/2005/Atom}content/'
                                 '{http://ws.constantcontact.com/ns/1.0/}ClickEvent/'
                                 '{http://ws.constantcontact.com/ns/1.0/}Contact')
            campaign = entry.find('{http://www.w3.org/2005/Atom}content/'
                                  '{http://ws.constantcontact.com/ns/1.0/}ClickEvent/'
                                  '{http://ws.constantcontact.com/ns/1.0/}Campaign')
            event = {'id': entry.findtext('{http://www.w3.org/2005/Atom}id'),
                     'updated': entry.findtext('{http://www.w3.org/2005/Atom}updated'),
                     'event_time': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                  '{http://ws.constantcontact.com/ns/1.0/}ClickEvent/'
                                                  '{http://ws.constantcontact.com/ns/1.0/}EventTime'),
                     'contact_id': contact.get('id'),
                     'contact_email_address': contact.findtext('{http://ws.constantcontact.com/ns/1.0/}EmailAddress'),
                     'campaign': campaign.get('id')
                     }
              
            events.append(event)
                     
        # If there is a next link, recursively retrieve from there too
        if(next_path != None):
            events.extend(self.__get_campaign_events_click_single_url(path=next_path))
            
        return events

    def get_activities(self, path=None):
        """ Returns all of the Activities from ConstantContact. """
        activities = []
        
        #get the namespaces for use locally
        atom = CTCTConnection.NS_ATOM
        ctct = CTCTConnection.NS_CTCT
    
        # Default path
        if(path == None):
            path = '/activities'
            
        response = self.connection.request_get(path)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))

        # Check if there is a next link
        links = xml.findall('{%s}link' % (atom));
        next_path = None
        for link in links:
            if(link.get('rel') == 'next'):
                next_link = link.get('href')
                slash = next_link.find('/activities')
                next_path = next_link[slash:]
                break
                
        # Get all of the activities
        entries = xml.findall('{%s}entry' % (atom))
        
        for entry in entries:
            activity = {'id': entry.findtext('{%s}id' % (atom)),
                        'updated': entry.findtext('{%s}updated' % (atom)),
                        'type': entry.findtext('{%s}content/{%s}Activity/{%s}Type' % (atom, ctct, ctct)),
                        'status': entry.findtext('{%s}content/{%s}Activity/{%s}Status' % (atom, ctct, ctct)),
                        'errors': entry.findtext('{%s}content/{%s}Activity/{%s}Errors' % (atom, ctct, ctct)),
                        'file_name': entry.findtext('{%s}content/{%s}Activity/{%s}FileName' % (atom, ctct, ctct)),
                        'transaction_count': entry.findtext('{%s}content/{%s}Activity/{%s}TransactionCount' % (atom, ctct, ctct)),
                        'run_start_time': entry.findtext('{%s}content/{%s}Activity/{%s}RunStartTime' % (atom, ctct, ctct)),
                        'run_finish_time': entry.findtext('{%s}content/{%s}Activity/{%s}RunFinishTime' % (atom, ctct, ctct)),
                        'insert_time': entry.findtext('{%s}content/{%s}Activity/{%s}InsertTime' % (atom, ctct, ctct))
                        }
            
            activities.append(activity)
            
        # If there is a next link, recursively retrieve from there too
        if(next_path != None):
            activities.extend(self.get_activities(path=next_path))
            
        return activities
        
    def get_activity(self, activity_id_number):
        """ Returns detailed information about an individual Activity 
            Requires the activity id number """
        
        #get the namespaces for use locally
        atom = CTCTConnection.NS_ATOM
        ctct = CTCTConnection.NS_CTCT
        
        activity_id = '/activities/' + str(activity_id_number)
        response = self.connection.request_get(activity_id)
        
        # If the status code isn't 200, we have a problem so just return None
        if(int(response['headers']['status']) != 200):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
        activity_xml = xml.find('{%s}content/{%s}Activity' % (atom, ctct))
        
        # Get all of the Errors this Activity has generated
        errors = []
        errors_xml = activity_xml.findall('{%s}Errors/{%s}Error' % (ctct, ctct))
        for error in errors_xml:
            errors.append({'line_number': error.findtext('{%s}LineNumber' % (ctct)),
                           'email_address': error.findtext('{%s}EmailAddress' % (ctct)),
                           'message': error.findtext('{%s}Message' % (ctct))
                            })
                           
        activity = {'id': xml.findtext('{%s}id' % (atom)),
                    'updated': xml.findtext('{%s}updated' % (atom)),
                    'type': activity_xml.findtext('{%s}Type' % (ctct)),
                    'status': activity_xml.findtext('{%s}Status' % (ctct)),
                    'errors': errors,
                    'file_name': activity_xml.findtext('{%s}FileName' % (ctct)),
                    'transaction_count': activity_xml.findtext('{%s}TransactionCount' % (ctct)),
                    'run_start_time': activity_xml.findtext('{%s}RunStartTime' % (ctct)),
                    'run_finish_time': activity_xml.findtext('{%s}RunFinishTime' % (ctct)),
                    'insert_time': activity_xml.findtext('{%s}InsertTime' % (ctct))
                    }
                    
        return activity

    def create_activity(self, type, lists, data=None, filename=None):
        """ Creates an activity to Add or Remove a large group of contacts
            to a list or multiple lists. The two supported request
            formats are application/x-www-form-urlencoded (raw data)
            and multipart/form-data (file) Returns Activity Id for 
            created activity """
        
        post_body = 'activityType=%s' % type
        
        if(filename is None):
            if(type is 'CLEAR_CONTACTS_FROM_LISTS'):
                for list in lists:
                    post_body += '&' + urlencode({'lists': list})
               
            elif(type in ['SV_ADD', 'ADD_CONTACTS', 'ADD_CONTACT_DETAIL', 'REMOVE_CONTACTS_FROM_LISTS']):
                if(data is not None):
                    post_body += '&data='
            
                    columns = data['columns']
                    rows = data['rows']
            
                    last_column = columns[-1]
                    for column in columns:
                        post_body += quote_plus(column)
                        post_body += '%2C' if column != last_column else '%0A'
            
                    index = 1
                    last_row = rows[-1]
                    values_per_row = len(rows[-1])
                    for row in rows:
                        for value in row:
                            post_body += quote(value) + '%2C' if index % values_per_row != 0 else quote(value)
                            index += 1
                        post_body += '%0A' if row != last_row else ''
                     
                    for list in lists:
                        post_body += '&' + urlencode({'lists': list})    
            
            elif(type is 'EXPORT_CONTACTS'):
                post_body += '&fileType=' + data['fileType'] if 'fileType' in data else '&fileType=TXT'
                post_body += '&exportOptDate=' + data['exportOptDate'] if 'exportOptDate' in data else '&exportOptDate=true'
                post_body += '&exportOptSource=' + data['exportOptSource'] if 'exportOptSource' in data else '&exportOptSource=true'
                post_body += '&exportListName=' + data['exportListName'] if 'exportListName' in data else '&exportListName=true'
                post_body += '&sortBy=' + data['sortBy'] if 'sortBy' in data else '&sortBy=EMAIL_ADDRESS'
                
                if('columns' in data):
                    for column in data['columns']:
                        post_body += '&' + urlencode({'columns': column})
                else:
                    post_body += '&columns=' + 'EMAIL%20ADDRESS'
                    
                for list in lists:
                    post_body += '&' + urlencode({'listId': list})

            response = self.connection.request_post('/activities', body=post_body, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        elif(filename is not None):
            #TODO: Add multipart/form-data bulk functionality
            return None
 
        # If the status code isn't 201, we have a problem so just return None
        if(int(response['headers']['status']) != 201):
            return None
        
        # Build an XML Tree from the return
        #xml = ET.fromstring(response['body'])
        xml = ET.fromstring(response['body'].encode('ascii','xmlcharrefreplace'))
            
        #return activity id of created activity
        activity_id = xml.findtext('{%s}id' % CTCTConnection.NS_ATOM)
            
        return activity_id
        