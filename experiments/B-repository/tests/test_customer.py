from src.customer import Customer, update_customer_email 
 
def test_update_customer_email_preserves_id_and_audit(): 
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin") 
    updated = update_customer_email(customer, "NEW@example.com", "agent") 
    assert updated.customer_id == 10 
    assert updated.created_by == "admin" 
    assert updated.updated_by == "agent" 
    assert updated.email == "new@example.com" 
 
def test_invalid_email_is_rejected(): 
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin") 
    try: 
        update_customer_email(customer, "invalid", "agent") 
        assert False 
    except ValueError as exc: 
        assert str(exc) == "invalid-email" 