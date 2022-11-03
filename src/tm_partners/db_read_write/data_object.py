class DataObject():
    def __init__(self, id, unit_no, floor, building, street, section, city, state, postcode, search_level_flag, source, source_id, salesman, notify_email, notify_mobile, result_type, result_remark, is_active, created_at, updated_at):
        self.id = id
        self.unit_no = unit_no
        self.floor = floor
        self.building = building
        self.street = street
        self.section = section
        self.city = city
        self.state = state
        self.postcode = postcode
        self.search_level_flag = search_level_flag
        self.source = source
        self.source_id = source_id
        self.salesman = salesman
        self.notify_email = notify_email
        self.notify_mobile = notify_mobile
        self.result_type = result_type
        self.result_remark = result_remark
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def get_id(self):
        return self.id
    
    def get_unit_no(self):
        return self.unit_no
    
    def get_floor(self):
        return self.floor

    def get_building(self):
        return self.building
    
    def get_street(self):
        return self.street
    
    def get_section(self):
        return self.section
    
    def get_city(self):
        return self.city
    
    def get_state(self):
        return self.state

    def get_postcode(self):
        return self.postcode

    def get_search_level_flag(self):
        return self.search_level_flag
    
    def get_source(self):
        return self.source
    
    def get_source_id(self):
        return self.source_id
    
    def get_salesman(self):
        return self.salesman

    def get_notify_email(self):
        return self.notify_email
    
    def get_notify_mobile(self):
        return self.notify_mobile
    
    def get_result_type(self):
        return self.result_type
    
    def get_result_remark(self):
        return self.result_remark
    
    def get_is_active(self):
        return self.is_active
    
    def get_created_at(self):
        return self.created_at
    
    def get_updated_at(self):
        return self.updated_at

