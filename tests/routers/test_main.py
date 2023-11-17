import pytest
from fastapi import status
from httpx import AsyncClient, Response


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response: Response = await async_client.post("/post", json={"body": body})
    return response.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    response: Response = await async_client.post(
        "/comment", json={"body": body, "post_id": post_id}
    )
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test Post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("Test Comment", created_post["id"], async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test Post"
    response: Response = await async_client.post("/post", json={"body": body})

    assert response.status_code == status.HTTP_201_CREATED
    assert {"id": 1, "body": body}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient):
    response: Response = await async_client.post("/post", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response: Response = await async_client.get("/post")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body: str = "Test Comment"
    response: Response = await async_client.post(
        "/comment", json={"body": body, "post_id": created_post["id"]}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert {
        "id": 1,
        "body": body,
        "post_id": created_post["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
) -> None:
    response: Response = await async_client.get(f"/post/{created_post['id']}/comment")

    # pytest has a way of parametrizing
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response: Response = await async_client.get(f"/post/{created_post['id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"post": created_post, "comments": [created_comment]}