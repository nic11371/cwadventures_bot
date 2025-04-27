from sqlalchemy import select, update, delete, desc
from database.models import User, Content, async_session


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
        return user


async def save_info_user(tg_id, address, comment, number):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.address = address
            user.comment = comment
            user.number = number
        await session.commit()


async def save_content_user(tg_id, content_id):
    async with async_session() as session:
        content = Content()
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            content.content_id = content_id
        await session.commit()
