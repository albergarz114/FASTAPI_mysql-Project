## Instructions:
NOTE: Please use mysql or sqlite.
Step 1. On Terminal: set up virtual environment -> python3 -m venv venv
Step 2. On Terminal: source venv/bin/activate
Step 3. On Terminal: pip3 install fastapi uvicorn sqlalchemy pymysql
Step 4. On Terminal: uvicorn main:app --reload


## unit testing
 pip3 install httpx
 pip3 install pytest
## Terminal -> Run 'pytest'

 ## Notes
def test_read_post_not_found():
    response = client.get("/posts/1")
    assert response.status_code == 404
    assert response.json() == {"detail":"Post 1 not found"}


def test_create_post():
    response = client.post(
        "/posts/",
        json={"title": "Albi", "content": "Great2", "user_id": 1}
    )
    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Albi"
    assert data["content"] == "Great2"   
    assert data["user_id"] == 1
    assert isinstance(data["id"], int)  


def test_update_post():
    # Create post
    create_response = client.post(
        "/posts/",
        json={"title": "Albi", "content": "Great2", "user_id": 1}
    )
    assert create_response.status_code == 201
    post_id = create_response.json()["id"]

    # Update the post
    response = client.put(
        f"/posts/{post_id}",
        json={"title": "Albi Updated", "content": "Great2", "user_id": 4}
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Post updated successfully"}



def test_delete_post():
    # Step 1: Create a post first
    create_response = client.post(
        "/posts/",
        json={"title": "Albi", "content": "Great2", "user_id": 1}
    )
    assert create_response.status_code == 201
    post_id = create_response.json()["id"]

    # Step 2: Delete the post
    delete_response = client.delete(f"/posts/{post_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data == {"message": "Post deleted successfully"}

    # Step 3: Verify the post no longer exists
    get_response = client.get(f"/posts/{post_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": f"Post {post_id} not found"}



## Notes over -> Unique = True (database/models.py)
## import random, string 

## Users
def test_read_user_not_found():
    response = client.get("/users/4")
    assert response.status_code == 404
    assert response.json() == {"detail": "User 4 not found"}


## for unique = True
def random_username():
    return "user_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))


def test_create_user():
    username = random_username()
    response = client.post("/users/", json={"username":username})

    assert response.status_code == 201
    data = response.json()

    assert data["username"] == username
    assert isinstance(data["id"], int) 


def test_update_user():
    # Create a user
    old_username = random_username()
    create_response = client.post("/users/", json={"username": old_username})
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Update the user
    new_username = random_username()
    response = client.put(f"/users/{user_id}", json={"username": new_username})
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "User updated successfully"}


def test_delete_user():
    # Step 1: Create a new user
    username = random_username()
    create_response = client.post("/users/", json={"username": username})
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Step 2: Delete the user
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "User deleted successfully"}

    # Step 3: Verify the user no longer exists
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": f"User {user_id} not found"}