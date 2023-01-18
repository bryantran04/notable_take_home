# notable_take_home

### Step 1: Build the docker image and containers

```
docker-compose up
```

### Step 2: Run Migrations inside python container

```
flask db init
flask db migrate
flask db upgrade
```

### Step 3: Hit endpoints at localhost

### Endpoints

- POST /patient

```
{
    "first_name": "p1",
    "last_name": "p2"
}
```

- POST /doctor

```
{
    "first_name": "d1",
    "last_name": "d2"
}
```

- GET /doctors

- POST /appointment

```
{
    "doctor_id": "1",
    "patient_id": "1",
    "appointment_datetime" : "09/19/22 13:00:00",
    "kind": "NEW_PATIENT" #ENUM [NEW_PATIENT, FOLLOW_UP]
}

```

- GET /doctor/<doctor_id>/appointments

- GET /doctor/<doctor_id>/appointments/<date> #09-20-2022

```
localhost/doctor/1/appointments/09-20-2022
```

- DELETE appointments/<appointment_id>
