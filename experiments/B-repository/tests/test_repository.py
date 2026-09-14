from src.customer import Customer 
from src.repository import CustomerRepository 
 
def test_update_email_requires_existing_customer(): 
    repo = CustomerRepository() 
    try: 
        repo.update_email(99, "a@example.com", "agent") 
        assert False 
    except ValueError as exc: 
        assert str(exc) == "customer-not-found" 
 
def test_repository_update_preserves_customer_id(): 
    repo = CustomerRepository() 
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin") 
    repo.add(customer) 
    repo.update_email(10, "new@example.com", "agent") 
    assert repo.get(10).customer_id == 10 