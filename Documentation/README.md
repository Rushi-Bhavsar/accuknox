## Assignment For AccuKnox.

- To Run the project just execute the docker command.
```shell
(venv) rushi@ubuntu:~/Study/accuknox$ docker build -f DockerFile . -t rushi1006/final_version_accuknox
(venv) rushi@ubuntu:~/Study/accuknox$ docker run -p 8010:8010 rushi1006/final_version_accuknox
```
- Basic Authentication via email and password is enabled.
- Set Basic Authentication in postman Authorization.

## Steps to call API
- First Do signup. **email and username are unique.** API {{base_url}}/api/sign_up/
- Login to cross verify. API ({{base_url}}/api/login/)
- Do Multiple SignUp. Create superuser using default management command. API {{base_url}}/api/sign_up/
- Check the profile view. API {{base_url}}/api/customer/{{user_id}}
- Check the profile view for admin user. API {{base_url}}/api/customer/
- Search connection using email. API {{base_url}}/api/search_connection/?search_name={{email}}
- Search connection using name. API {{base_url}}/api/search_connection/?search_name={{name}}
- List all profile present. API {{base_url}}/api/search_connection/
- Send multiple new connection request. API {{base_url}}/api/send_connection_request/
- Accept connection request. API {{base_url}}/api/process_request/
- Reject connection request. API {{base_url}}/api/process_request/
- List all pending connection request. API {{base_url}}/api/connection_request_status/?status=pending
- List all rejected connection request. API {{base_url}}/api/connection_request_status/?status=reject
- List all friends list. API {{base_url}}/api/friends/


## Below are only happy flow api responses.

**base_url = http://127.0.0.1:8000**
## SignUp Customer on-boarding.
- End Point **{{base_url}}/api/sign_up/**
```json
{
    "code": 100,
    "msg": "New User Created successfully",
    "customer_id": 20
}
```

## Login API Done.
- End Point **{{base_url}}/api/login/**
```json
{
    "msg": "Login Successful for Customer: rushi@gmail.com"
}
```

## API to search by email with pagination
- End Point **{{base_url}}/api/search_connection/?search_name=devesh.kulkarni@gmail.com**
```json
{
    "code": 100,
    "msg": "Search Details",
    "total_count": 1,
    "page_count": 1,
    "next": null,
    "previous": null,
    "result": [
        {
            "username": "devesh_kulkarni",
            "pk": 15
        }
    ]
}
```

## API to search by first_name with pagination
- End Point **{{base_url}}/api/search_connection/?search_name=a**
```json
{
    "code": 100,
    "msg": "Search Details",
    "total_count": 15,
    "page_count": 10,
    "next": "http://127.0.0.1:8000/api/search_connection/?page=2&search_name=a",
    "previous": null,
    "result": [
        {
            "username": "harshal",
            "pk": 2
        },
        {
            "username": "vishal_patil",
            "pk": 3
        },
        {
            "username": "vishal_dhande",
            "pk": 4
        },
        {
            "username": "mayur_kulkarni",
            "pk": 5
        },
        {
            "username": "keval_thakkar",
            "pk": 6
        },
        {
            "username": "devina_yadav",
            "pk": 7
        },
        {
            "username": "ashwini_ghure",
            "pk": 8
        },
        {
            "username": "rahul_haral",
            "pk": 9
        },
        {
            "username": "harsh_jain",
            "pk": 10
        },
        {
            "username": "mandar_bhavsar",
            "pk": 11
        }
    ]
}
```

## API to display all the customer incase email and first_name is not mentioned with pagination.
- End Point **{{base_url}}/api/search_connection/**
```json
{
    "code": 100,
    "msg": "Search Details",
    "total_count": 18,
    "page_count": 10,
    "next": "http://127.0.0.1:8000/api/search_connection/?page=2",
    "previous": null,
    "result": [
        {
            "username": "harshal",
            "pk": 2
        },
        {
            "username": "vishal_patil",
            "pk": 3
        },
        {
            "username": "vishal_dhande",
            "pk": 4
        },
        {
            "username": "mayur_kulkarni",
            "pk": 5
        },
        {
            "username": "keval_thakkar",
            "pk": 6
        },
        {
            "username": "devina_yadav",
            "pk": 7
        },
        {
            "username": "ashwini_ghure",
            "pk": 8
        },
        {
            "username": "rahul_haral",
            "pk": 9
        },
        {
            "username": "harsh_jain",
            "pk": 10
        },
        {
            "username": "mandar_bhavsar",
            "pk": 11
        }
    ]
}
```

## API to display all customer profile view with pagination only for superuser and staff user.
- End Point **{{base_url}}/api/customer/**
```json
{
    "code": 100,
    "msg": "All user list",
    "total_count": 20,
    "page_count": 10,
    "next": "http://127.0.0.1:8000/api/customer/?page=2",
    "previous": null,
    "result": [
        {
            "id": 1,
            "email": "rushi@gmail.com",
            "username": "rushi_1006",
            "first_name": "Rushikesh",
            "last_name": "Bhavsar",
            "is_active": true
        },
        {
            "id": 2,
            "email": "hasrshal@gmail.com",
            "username": "harshal",
            "first_name": "Harshal",
            "last_name": "Wagh",
            "is_active": true
        },
        {
            "id": 3,
            "email": "vishal.patil@gmail.com",
            "username": "vishal_patil",
            "first_name": "Vishal",
            "last_name": "Patil",
            "is_active": true
        },
        {
            "id": 4,
            "email": "vishal.dhande@gmail.com",
            "username": "vishal_dhande",
            "first_name": "Vishal",
            "last_name": "dhande",
            "is_active": true
        },
        {
            "id": 5,
            "email": "mayur.kulkarni@gmail.com",
            "username": "mayur_kulkarni",
            "first_name": "Mayur",
            "last_name": "Kulkarni",
            "is_active": true
        },
        {
            "id": 6,
            "email": "keval.thakkar@gmail.com",
            "username": "keval_thakkar",
            "first_name": "Keval",
            "last_name": "Thakkar",
            "is_active": true
        },
        {
            "id": 7,
            "email": "devina.yadav@gmail.com",
            "username": "devina_yadav",
            "first_name": "Devina",
            "last_name": "Yadav",
            "is_active": true
        },
        {
            "id": 8,
            "email": "ashwini.ghure@gmail.com",
            "username": "ashwini_ghure",
            "first_name": "Ashwini",
            "last_name": "Ghure",
            "is_active": true
        },
        {
            "id": 9,
            "email": "rahul.haral@gmail.com",
            "username": "rahul_haral",
            "first_name": "Rahul",
            "last_name": "Haral",
            "is_active": true
        },
        {
            "id": 10,
            "email": "hasrh.jain@gmail.com",
            "username": "harsh_jain",
            "first_name": "Harsh",
            "last_name": "Jain",
            "is_active": true
        }
    ]
}
```

## API to send new connection request
- End Point **{{base_url}}/api/send_connection_request/**
```json
{
    "msg": "Request Send from rushi@gmail.com to rahul.haral@gmail.com"
}
```

## API to approve new connection request
- End Point **{{base_url}}/api/process_request/**
```json
{
    "msg": "Connection added."
}
```

## API to reject new connection request
- End Point **{{base_url}}/api/process_request/**
```json
{
    "msg": "Connection Rejected"
}
```

## API to list all friends for specific user.
- End Point **{{base_url}}/api/sign_up/**
```json
{
    "code": 100,
    "msg": "Details found.",
    "total_count": 5,
    "page_count": 5,
    "next": null,
    "previous": null,
    "result": [
        {
            "to_user": 2,
            "customer_username": "harshal"
        },
        {
            "to_user": 3,
            "customer_username": "vishal_patil"
        },
        {
            "to_user": 4,
            "customer_username": "vishal_dhande"
        },
        {
            "to_user": 5,
            "customer_username": "mayur_kulkarni"
        },
        {
            "to_user": 11,
            "customer_username": "mandar_bhavsar"
        }
    ]
}
```

## API to check all pending / rejected connection request.
- End Point **{{base_url}}/api/connection_request_status/?status=pending**
```json
{
    "code": 100,
    "msg": "Requested Details found.",
    "total_count": 3,
    "page_count": 3,
    "next": null,
    "previous": null,
    "result": [
        {
            "receiver_user": 13,
            "status": "pending"
        },
        {
            "receiver_user": 14,
            "status": "pending"
        },
        {
            "receiver_user": 15,
            "status": "pending"
        }
    ]
}
```

## API to check all rejected connection request.
- End Point **{{base_url}}/api/connection_request_status/?status=reject**
```json
{
    "code": 100,
    "msg": "Requested Details found.",
    "total_count": 3,
    "page_count": 3,
    "next": null,
    "previous": null,
    "result": [
        {
            "receiver_user": 6,
            "status": "reject"
        },
        {
            "receiver_user": 9,
            "status": "reject"
        },
        {
            "receiver_user": 12,
            "status": "reject"
        }
    ]
}
```

## User can send more than 3 new connection request in 1 min.
- End Point **{{base_url}}/api/send_connection_request/**
```json
{
    "msg": "Can not send more than 3 new connection request within 1 min."
}
```

- All the above API are done.
