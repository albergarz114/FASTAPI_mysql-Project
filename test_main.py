from fastapi.testclient import TestClient
import random, string #for unique = True
from main import app
client = TestClient(app)

from sqlalchemy.orm import declarative_base
Base = declarative_base()


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


def test_get_beers_not_found():
    response = client.get("/beers/20")
    assert response.status_code == 404
    assert response.json() == {"detail":"Item 20 not found"}


def test_create_beer():
    response = client.post("/beers/", json={"style": "Ale", "alcohol": True, "cereal":"barley malt"})

    assert response.status_code == 201
    data = response.json()

    assert data["style"] == "Ale"
    assert data["alcohol"] == True
    assert data["cereal"] == "barley malt"
    assert isinstance(data["id"], int)


def test_update_beer():

    create_response = client.post("/beers/", json={"style": "Ale", "alcohol": True, "cereal":"barley malt"})
    assert create_response.status_code == 201
    beer_id = create_response.json()["id"]
    

    response = client.put(f"/beers/{beer_id}", json={"style": "Lager", "alcohol": False, "cereal":"barley malt, wheat"})
    assert response.status_code == 200
    data = response.json()
    assert data == {"message":"Item updated successfully"}
    


def test_delete_beer():

    create_response = client.post("/beers/", json={"style": "Ale", "alcohol": True, "cereal":"barley malt"})
    assert create_response.status_code == 201
    beer_id = create_response.json()["id"]
    

    delete_response = client.delete(f"/beers/{beer_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data == {"message":"Item deleted successfully"}

    get_response = client.get(f"/beers/{beer_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail":f"Item {beer_id} not found"}


## teas
def test_get_tea_not_found():
    response = client.get("/teas/200")
    assert response.status_code == 404
    assert response.json() == {"detail":"Item 200 not found"}


def test_create_tea():
    response = client.post("/teas/", json={"style":"White", "healthy": True})
    assert response.status_code == 201
    data = response.json()
    
    assert data["style"] == "White"
    assert data["healthy"] == True
    assert isinstance(data["id"], int)


def test_update_tea():

    create_response = client.post("/teas/", json={"style":"White", "healthy": True})
    assert create_response.status_code == 201
    tea_id = create_response.json()["id"]

    response = client.put(f"/teas/{tea_id}", json={"style":"Earl Grey", "healthy": False})
    assert response.status_code == 200
    data = response.json()
    assert data == {"message":"Item updated successfully"}


def test_delete_tea():

    create_response = client.post("/teas/", json={"style":"White", "healthy": True})
    assert create_response.status_code == 201
    tea_id = create_response.json()["id"]

    delete_response = client.delete(f"/teas/{tea_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data == {"message":"Item deleted successfully"}

    get_response = client.get(f"/teas/{tea_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail":f"Item {tea_id} not found"}


#Products
def test_get_products_not_found():
    response = client.get("/products/200")
    assert response.status_code == 404
    assert response.json() == {"detail":"Item 200 not found"}



def test_create_product():
    create_response = client.post("/products/", json={"name":"Alberto", "price": 23.50})

    assert create_response.status_code == 201
    data = create_response.json()

    assert data["name"] == "Alberto"
    assert data["price"] == 23.50
    assert isinstance(data["id"], int)


def test_update_product():

    create_response = client.post("/products/", json={"name":"Alberto", "price": 23.50})
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    response = client.put(f"/products/{product_id}", json={"name":"Al", "price": 28.00})
    assert response.status_code == 200
    data = response.json()
    assert data == {"message":"Item updated successfully"}


def test_delete_product():

    create_response = client.post("/products/", json={"name":"Alberto", "price": 23.50})
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data == {"message":"Item deleted successfully"}

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail":f"Item {product_id} not found"}