"""
Test command:
docker exec -it nowa_pochta-web-1 pytest --cov
"""
import json


# def test_task_status(test_app):
#     response = test_app.get("/")
#     content = response.json()
#     assert content == {"message": "Hello World"}
#     assert response.status_code == 200


def test_get_warehouses(test_app):
    response = test_app.get("/warehouses?city_ref=e7182b3c-4b33-11e4-ab6d-005056801329")
    content = response.json()
    assert len(content["warehouses"]) > 0
    assert response.status_code == 200


# def test_get_warehouses(test_app):
#     response = test_app.get("/warehouses?city_ref=e7182b3c-4b33-11e4-ab6d-005056801329")
#     content = response.json()
#     assert content["warehouses"][0] == "Відділення №1: вул. Максимовича, 8"
#     assert response.status_code == 200


# def test_task_status(test_app):
#     response = test_app.post(
#         "/tasks",
#         data=json.dumps({"type": 1})
#     )
#     content = response.json()
#     task_id = content["task_id"]
#     assert task_id

#     response = test_app.get(f"tasks/{task_id}")
#     content = response.json()
#     assert content == {"task_id": task_id, "task_status": "PENDING", "task_result": None}
#     assert response.status_code == 200

#     while content["task_status"] == "PENDING":
#         response = test_app.get(f"tasks/{task_id}")
#         content = response.json()
#     assert content == {"task_id": task_id, "task_status": "SUCCESS", "task_result": True}