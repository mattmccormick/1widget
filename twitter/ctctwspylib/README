Copyright 1996-2009 Constant Contact, Inc. All rights reserved.
    
Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at 
    
    http://www.apache.org/licenses/LICENSE-2.0 
        
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License. 

Python Client Library - Documentation

For more information regarding the Constant Contact APIs visit:
    http://developer.constantcontact.com/doc/reference

-----Creating the Connection Object-----

Using the client library starts with creating a CTCTConnection object.  You must supply a Constant Contact username and password as well as a Constant Contact developer key.  If you don't have an account you can create one here: https://www.constantcontact.com/features/signup.jsp.  And Constant Contact API keys are requested here: http://developer.constantcontact.com/license/login.

    API_KEY = "ctctabc-defghi-jklmnop" #not a valid key
    mConnection = CTCTConnection(API_KEY, "joe", "password123")

-----Authentication-----

To authenticate credentials, in this case joe using password123, you might do the following:

    isValid = mConnection.verify_credentials()

    if(isValid):
        #valid credentials
    else:
        #invalid credentials
    
Characters outside the character set a-zA-Z0-9.-_@ are not allowed in Constant Contact usernames. Using the library you are able to catch this:

    try:
        isValid = connObject.verify_credentials()
    except connObject.InvalidUsernameException, err:  #err contains an appropriate error message
        print str(err)
    
-----Contact Lists-----

**Retrieve ALL Lists.  

Fields retrieved are: 
    id 
    name
    updated
    
Lists NOT returned:    
    Removed
    Do Not Mail 
    Active

    #lists will contain a python list of dictionaries, each dictionary contains data for an individual list
    lists = mConnection.get_contact_lists()

    #print all the list names
    for list in lists:
        print list['name']

**Retrieve Individual List.  

Lists are retrieved using the list id.  

Fields retrieved are 
    id 
    name
    updated
    opt_in_default
    short_name
    sort_order.

    list_id = '123'
    list = mConnection.get_contact_list(list_id)

    #print the list name
    print list['name']

**Retrieve List Members.  

The list members are returned in a python list of dictionaries, each containing individual contact information.  

Fields retrieved are 
    id
    name
    email_address
    updated

    list_id = '123'
    #get the members of list 123
    members = mConnection.get_contact_list_members(list_id)

    #print the emails of all the members in list 123
    for member in members:
        print member['email_address']

**Creating a New List

To create a new list simply pass a list name.

    #name of list to create
    name = 'My New List'

    #create the contact, wasCreated holds success
    wasCreated = mConnection.create_contact_list(name)

**Update a List

Update a list by passing the list id and a python dictionary containing the fields and values to update.

    #list id to update
    list_id = '123'
    
    #specify parameters to change
    params = {'name': 'New List Name'}

    #update the list, wasUpdated holds succecss
    wasUpdated = mConnection.update_contact_list(params, list_id)

**Delete a List

To delete a list use the list id.

    #list id to delete
    list_id = '123'

    #delete list 123, wasDeleted holds success
    wasDeleted = mConnection.delete_contact_list(list_id)

-----Contacts-----

**Retrieve ALL Contacts

Fields retrieved are: 
    id
    email_address
    email_type
    name
    opt_in_source
    updated

    #retrieve all the contacts
    contacts = mConnection.get_contacts()

    #print the email addresses of all contacts
    for contact in contacts:
        print contact['email_address']
    
**Retrieve Individual Contact

Retrieve detailed information about a contact by providing either a contact email address or a contact id.  If both the contact id and email address are available use the id.  

Fields returned are:
    id
    updated
    status
    email_address
    email_type
    name
    first_name
    middle_name
    last_name
    job_title
    company_name
    home_phone
    work_phone
    addr1
    addr2
    addr3
    city
    state_code
    state_name
    country_code
    country_name
    postal_code
    sub_postal_code
    note
    custom_field1
    ...
    custom_field15
    contact_lists
    
    #get the contact by email
    contact = mConnection.get_contact(email='joe@sampleaddress.com')
    
    #get the contact by id
    contact = mConnection.get_contact(contact_id_number='123')
    
    #get the contact lists the contact is a member of
    lists = contact['contact_lists']
    
    #print all the lists ids the contact belongs to
    for list in lists:
        print list['id']

**Create A Contact

To create a contact supply a dictionary of parameters, keys containting fields to add and corresponding values. Id will be created automatically so do not include it.

#add the fields
params = {'email_address': 'joe@samplename.com', 'name': 'joe', 'home_phone': '9785554444'}

#create the contact and store success
wasCreated = mConnection.create_contact(params)

**Update A Contact

Updating an existing contact requires a dictionary of paramaters, fields to change with changed values, and the contact id or contact email address. Again, contact id is preferred.

    #contact id to update
    contact_id = '123'

    #fields to update, note that new fields can also be added this way
    params = {'name': 'joey', 'home_phone': '9783334545', 'city': 'New York'}

    #update the contact using the contact id, and store success
    wasUpdated = mConnection.update_contact(params, contact_id_number=contact_id)

    #update the contact using an email address, ..
    wasUpdated = mConnection.update_contact(params, email='joe@samplename.com')

**Deleting A Contact

To delete a contact all that is needed is the contact id or email address of the contact.

    #contact id to delete
    contact_id = '123'

    #delete the contact using the contact id (preferred)
    wasDeleted = mConnection.delete_contact(contact_id_number=contact_id)

    #delete the contact using the email address
    wasDeleted = mConnection.delete_contact(email='joe@samplename.com') 

**Retrieve Contact Events

To retrieve events for a contact specify the contact either by email address or contact id and the event type.  Event type is an enumeration of the CTCTConnection class.

Event types are:
    EVENTS_BOUNCES (0)
    EVENTS_CLICKS
    EVENTS_FORWARDS
    EVENTS_OPENS
    EVENTS_OUT_OUTS 
    EVENTS_SENDS (5)
    
    #get the number of bounce events for contact 123
    bounce_events = mConnection.get_contact_events(event_type=CTCTConnection.EVENTS_BOUNCES, contact_id_number=123)
    
    #get the number of opens for joe@samplename.com
    open_events = mConnection.get_contact_events(event_type=CTCTConnection.EVENTS_OPENS, email='joe@samplename.com')
    
-----Campaigns-----

**Retrieve ALL Campaigns

To retrieve all campaigns specify the type of campaigns to be returned.  If no campaign type is specified, ALL will be returned.  A python list of campaigns will be returned and each campaign in campaigns is a dictionary containing fields and values for each individual campaign.  

Fields returned are:
    id
    name
    status
    date
    updated
    
Campaign type is an enumeration of the CTCTConnection class.

Campaign types are:
    CAMPAIGNS_ALL (0)
    CAMPAIGNS_DRAFT
    CAMPAIGNS_RUNNING
    CAMPAIGNS_SENT
    CAMPAIGNS_SCHEDULED (4)
    
    #get all sent campaigns
    sent_campaigns = mConnection.get_campaigns(type=CTCTConnection.CAMPAIGNS_SENT)
    
    #print the date for all sent campaigns
    for campaign in sent_campaigns:
        print campaign['date']
 
**Get An Individual Campaign

To retrieve an individual campaign just pass the campaign id.  A dictionary containing the invidual campaign data will be returned.

Fields returned are:
    id
    updated
    status
    name
    date
    last_edit_date
    last_run_date
    sent
    opens
    clicks
    bounces
    forwards
    opt_outs
    spam_reports
    contact_lists
    urls

   campaign_id = '1234567890123'
   
   #get the campaign by id
   campaign = mConnection.get_campaign(campaign_id_number=campaign_id)
   
   #print the campaign name
   print 'The Campaign Name is ' + campaign['name']
   
   #print the contact lists associated with the email campaign
   lists = campaign['contact_lists']
   for list in lists:
       print list['id']
       
   #print the campaign-included urls clicks tracking information
   urls = campaign['urls']
   for url in urls:
       print url['clicks']
       
**Get Campaign Events

To retrieve events for a campaign specify the campaign id and the event type.  Event type is an enumeration of the CTCTConnection class.

Event types are:
    EVENTS_BOUNCES (0)
    EVENTS_CLICKS
    EVENTS_FORWARDS
    EVENTS_OPENS
    EVENTS_OUT_OUTS 
    EVENTS_SENDS (5)

    #get the bounce events for the campaign
    bounce_events = mConnection.get_campaign_events('123456789123', CTCTConnection.EVENTS_BOUNCES)    
   
    #get the total sends for the campaign
    sent = mConnection.get_campaign_events('12345678123', CTCTConnection.EVENTS_SENDS)
    
-----Activities-----

**Retrieve ALL Activities

Fields returned are:
    id
    updated
    type
    status
    errors
    file_name
    transaction_count
    run_start_time
    run_finish_time
    insert_time
    
    #get all activities
    activities = mConnection.get_activities()
    
    #print the status for all activities
    for activity in activities:
        print activity['status']
        
**Get An Individual Activity

To retrieve an individual activity just pass the activity id.  A dictionary containing the invidual activity data will be returned.

Fields returned are:    
    id
    updated
    type
    status
    errors
    file_name
    transaction_count
    run_start_time
    run_finish_time
    insert_time
    
    #not a real activity id, for example
    activity_id = '1234567890123'
    
    #get the individual activity
    activity = mConnection.get_activity(activity_id_number=activity_id)
    
    #print the errors for the activity if there are any
    errors = activity['errors']
    for error in errors:
        print error
        
**Creating an Add Contacts / Remove Contacts Activity

To create an Add or Remove Contacts activity you must supply a type (Add or Remove), the lists you would like to add to or remove from, and the actual contact data to be added or removed.  The activity id is returned or None if it was unsuccessful

The types are: ADD_CONTACTS, SV_ADD, ADD_CONTACT_DETAIL, REMOVE_CONTACTS_FROM_LISTS. Constant Contact will decide which Add to use depending on the data so using any of the three add types will yield the same result.  To remove contacts from lists use REMOVE_CONTACTS_FROM_LISTS.
    
The data has to be supplied in a tabular format.  The first row is always the column names and each row after that is the data for each contact in the same order as the supplied columns. For example:

EMAIL ADDRESS,  FIRST NAME, LAST NAME
num1@email.com, Joe,        Smith
num2@email.com, Jane,       Smith
...

In python, there is a dictionary containting a key columns and a key rows that contain the values in python lists.  The lists will contain the column data and row data respectively.

    #lists contacts will be added to
    lists = ['http://api.constantcontact.com/ws/customers/username/lists/1', 'http://api.constantcontact.com/ws/customers/username/lists/2']
    
    #data to be added to the lists, email address, first name
    data = {'columns': ['EMAIL ADDRESS', 'FIRST NAME'], 'rows': ['num1@email.com', 'Joe']}
    
    #create the add contact activity, the activity id is returned if successful
    activity_id = mConnection.create_activity(type='SV_ADD', lists=lists, data=data)
    
    #check the activity status
    activity = mConnection.get_activity(activity_id_number=activity_id)
    print activity['status']
    
**Creating a Clear Contacts Activity

A Clear Contacts activity is different than a Remove Contacts activity. It will clear all contacts from a list or lists.  To create the activity just supply the lists to be cleared. The activity id is returned.

    #lists to clear
    lists = ['http://api.constantcontact.com/ws/customers/username/lists/1', 'http://api.constantcontact.com/ws/customers/username/lists/1']

    #create clear contacts activity
    activity_id = mConnection.create_activity(type='CLEAR_CONTACTS_FROM_LISTS', lists=lists)
    
    #check the activity status
    activity = mConnection.get_activity(activity_id_number=activity_id)
    print activity['status']
    
**Creating a Export Contacts Activity

A Export activity exports contacts from a list or lists to a txt or csv file.  To create the activity just supply the type of EXPORT_CONTACTS and a list to export. Additionally you can also supply options which are passed in the 'data' parameter. Options are dictionary entries with the key being the keynames below and the corresponding value options.

Options (defaults are bold):
        fileType        csv or txt
        exportOptDate   true or false
        exportOptSource true or false
        exportListName  true or false
        sortBy          EMAIL_ADDRESS, DATE_DESC
        columns         FIRST NAME, MIDDLE NAME, LAST NAME, etc... complete list see http://developer.constantcontact.com/doc/activities
        
        #the list to export
        lists = {'list_id': 'http://api.constantcontact.com/ws/customers/username/lists/1'}
        
        #the columns to export, email address is always exported by default
        data = {'columns': ['First Name', 'Last Name']}
        
        #create an export activity as a csv file sorting the columns by date descending
        activity_id = mConnection.create_activity(type='EXPORT_CONTACTS', lists=lists, data=data)
        
        #check the activity status
        activity = mConnection.get_activity(activity_id_number=activity_id)
        print activity['status']