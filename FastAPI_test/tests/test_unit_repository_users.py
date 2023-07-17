import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email(self):
        user = User(email="test")
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="test", db=self.session)
        self.assertEqual(result.email, user.email)

    async def test_create_user(self):
        body = UserModel(username="test", email="test", password="password")
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    async def test_update_token(self):
        user = User()
        refresh_token = "1.1.1"
        await update_token(user=user, token=refresh_token, db=self.session)
        self.assertEqual(user.refresh_token, refresh_token)

    async def test_confirmed_email(self):
        user = User(email="test")
        self.session.query().filter().first.return_value = user
        await confirmed_email(email="test", db=self.session)
        self.assertEqual(user.confirmed, True)

    async def test_update_avatar(self):
        user = User(email="test")
        self.session.query().filter().first.return_value = user
        url = "test"
        await update_avatar(email="test", url=url, db=self.session)
        self.assertEqual(user.avatar, url)


if __name__ == '__main__':
    unittest.main()