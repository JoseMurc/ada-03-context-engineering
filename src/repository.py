from src.customer import Customer, update_customer_email 
 
class CustomerRepository: 
    def __init__(self): 
        self.customers = {} 
 
    def add(self, customer): 
        self.customers[customer.customer_id] = customer 
 
    def get(self, customer_id): 
        return self.customers.get(customer_id) 
 
    def save(self, customer): 
        self.customers[customer.customer_id] = customer 
 
    def update_email(self, customer_id, new_email, updated_by): 
        customer = self.get(customer_id) 
        if customer is None: 
            raise ValueError("customer-not-found") 
        customer = update_customer_email(customer, new_email, updated_by) 
        self.save(customer) 
        return customer 