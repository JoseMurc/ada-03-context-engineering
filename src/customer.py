from dataclasses import dataclass 
 
@dataclass 
class Customer: 
    customer_id: int 
    name: str 
    email: str 
    created_by: str 
    updated_by: str 
 
def update_customer_email(customer, new_email, updated_by): 
    if "@" not in new_email: 
        raise ValueError("invalid-email") 
    customer.email = new_email.lower() 
    customer.updated_by = updated_by 
    return customer 