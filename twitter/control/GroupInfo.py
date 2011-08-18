class GroupInfo:
    
    def __init__(self, user):
        self.group = user.groups.all()[0]
        
    def __unicode__(self):
        return self.group.name
        
    def is_free(self):
        return self.group.id == 1
    
    def is_paid(self):
        return not self.is_free(self)
 
    def get_digests_limit(self):
        options = {'Free': 1,
                   'Small': 5,
                   'Multi': 25,
                   'Premium': 100}
        
        return options[self.group.name]
        
    def get_feeds_limit(self):
        options = {'Free': 5,
                   'Small': 25,
                   'Multi': 100,
                   'Premium': 1000000}
        
        return options[self.group.name]
    
    def get_feeds_limit_str(self):
        options = {'Free': '5',
                   'Small': '25',
                   'Multi': '100',
                   'Premium': 'Unlimited'}
        
        return options[self.group.name]
    
    def get_views_limit(self):
        options = {'Free': 1000,
                   'Small': 5000,
                   'Multi': 25000,
                   'Premium': 100000}
        
        return options[self.group.name]