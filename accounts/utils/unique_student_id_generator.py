import random
import string

def generate_student_id():
    # 1. Create the initial base ID
    base_id = f"ID-{random.randint(1000, 9999)}"
    
    # 2. Loop until we find a version that doesn't exist in the DB
    from accounts.models import Account
    while Account.objects.filter(student_id=base_id).exists():
        # Generate 3 random letters/numbers to append
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        base_id = f"{base_id}-{suffix}"
        
        # Optional: break if suffix still hits a duplicate (rare, but safer)
        # The loop will re-run and add another suffix if needed
        
    return base_id

