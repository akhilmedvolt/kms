(No direct FK relationship from User → Lead in the example code. 
 If needed, you could add a user_id FK on Lead to represent who owns/manages each Lead.)

┌───────────────┐
│    User       │
├───────────────┤
│ id (PK)       │
│ username      │
│ hashed_password
│ is_active     │
└───────────────┘


             (1)              (1)  ┌─────────────────────────┐
User -------- (?)           (?) ---->  Lead                  │
                                  ├─────────────────────────┤
                                  │ id (PK)                │
                                  │ restaurant_name        │
                                  │ status                 │
                                  │ call_frequency_days    │
                                  │ last_call_date         │
                                  └─────────┬──────────────┘
                                            │ (1 - many)
                                            ▼
                          ┌─────────────────────────┐
                          │        Contact         │
                          ├─────────────────────────┤
                          │ id (PK)                │
                          │ name                   │
                          │ role                   │
                          │ contact_info           │
                          │ lead_id (FK → Lead.id) │
                          └─────────┬──────────────┘
                                    │ (1 - many)
                                    ▼
                          ┌─────────────────────────┐
                          │     Interaction        │
                          ├─────────────────────────┤
                          │ id (PK)                │
                          │ interaction_date       │
                          │ details                │
                          │ type                   │
                          │ lead_id (FK → Lead.id) │
                          └─────────────────────────┘
