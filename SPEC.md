# Customer Email Update 
 
## Goal 
Allow an existing customer to update their email address safely. 
 
## Requirements 
1. Customer must exist. 
2. New email must be lowercase. 
3. New email must be syntactically valid. 
4. Customer ID must never change. 
5. created_by must be preserved. 
6. updated_by must contain the actor performing the update. 
7. Existing behavior and tests must remain valid. 
 
## Acceptance Criteria 
- Valid email -> update succeeds and is lowercase. 
- Invalid email -> ValueError("invalid-email"). 
- Missing customer -> ValueError("customer-not-found"). 
- Customer ID and created_by remain unchanged. 
