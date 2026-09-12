from datetime import datetime


class CHPVisit:
    def __init__(self, visit_id, chp_id, client_id, visit_date=None, notes=""):
        self.visit_id = visit_id
        self.chp_id = chp_id
        self.client_id = client_id
        self.visit_date = visit_date or datetime.now()
        self.notes = notes
