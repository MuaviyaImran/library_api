from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    return {"message": "Library Management API is running!"}
