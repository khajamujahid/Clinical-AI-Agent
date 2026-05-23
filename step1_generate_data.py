import os
import random
from faker import Faker

fake = Faker()
os.makedirs("clinical_notes", exist_ok=True)

conditions = ["Type 2 Diabetes", "Hypertension", "Atrial Fibrillation", "Asthma", "Osteoarthritis"]
medications = ["Metformin", "Lisinopril", "Amlodipine", "Albuterol", "Ibuprofen"]

print("Generating simulated clinical notes...")
for i in range(50):
    patient_id = fake.uuid4()[:8]
    condition = random.choice(conditions)
    medication = random.choice(medications)
    
    note_content = f"""
    Patient ID: {patient_id}
    Date of Birth: {fake.date_of_birth(minimum_age=30, maximum_age=90).strftime('%Y-%m-%d')}
    Date of Visit: {fake.date_this_year().strftime('%Y-%m-%d')}
    
    Chief Complaint: Patient presents with ongoing management of {condition}.
    
    Assessment & Plan:
    1. {condition}: Continue current care plan.
    2. Prescriptions: Refill {medication} 10mg daily.
    
    Provider: Dr. {fake.last_name()}
    """
    
    with open(f"clinical_notes/note_{patient_id}.txt", "w") as file:
        file.write(note_content)

print("✅ 50 mock clinical notes generated in the 'clinical_notes' folder!")