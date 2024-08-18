import pytest
from faker import Faker
from datetime import datetime
from unittest.mock import patch

from src.modules.shared.di import (
    auth_service,
    user_service,
    email_service,
    session_service,
    verification_token_service,
)
from src.modules.auth.models import TokenType

def _prepare_user_data():
    fake = Faker()
    data = {
        "name": fake.name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
    }
    return data

@pytest.fixture(scope="function", autouse=True)
def mock_send_email():
    with patch.object(email_service, 'send_email') as mock:
        mock.return_value = True
        yield mock


def test_auth_signup_with_invalid_password():
    data = _prepare_user_data()
    data["password"] = "invalidpassword"
    result = auth_service.signup(data)
    assert result == False


def test_auth_signup_with_invalid_email():
    data = _prepare_user_data()
    data["email"] = "invalidemail"
    result = auth_service.signup(data)
    assert result == False


def test_auth_signup(mock_send_email):
    data = _prepare_user_data()
    result = auth_service.signup(data)
    assert result == True
    created_user = user_service.get_by_email(data["email"])
    assert created_user is not None
    assert str(created_user.email) == data["email"]
    assert str(created_user.name) == data["name"]
    assert str(created_user.last_name) == data["last_name"]
    mock_send_email.assert_called_once()


def test_auth_verify_signup():
    data = _prepare_user_data()
    result = auth_service.signup(data)
    assert result == True
    created_user = user_service.get_by_email(data["email"])
    token = verification_token_service.get_by_user_id(
        str(created_user.id), TokenType.SIGNUP)
    assert token is not None
    assert str(token.user_id) == str(created_user.id)
    assert token.is_signup == True
    assert token.is_expired == False
    assert token.is_verified == False
    result = auth_service.verify_signup(str(token.token))
    assert result == True
    created_user = user_service.get_by_email(data["email"])
    assert created_user is not None
    assert created_user.is_active == True
    verified_token = verification_token_service.get_by_user_id(
        str(created_user.id), TokenType.SIGNUP)
    assert verified_token is not None
    assert verified_token.is_verified == True

def test_auth_signin_with_invalid_email():
    data = _prepare_user_data()
    data["email"] = "invalidemail"
    result = auth_service.signin(data)
    assert result == False


def test_auth_signin_with_invalid_password():
    data = _prepare_user_data()
    data["password"] = "invalidpassword"
    result = auth_service.signin(data)
    assert result == False


def test_auth_signin():
    data = _prepare_user_data()
    auth_service.signup(data.copy())
    created_user = user_service.get_by_email(data["email"])
    token = verification_token_service.get_by_user_id(
        str(created_user.id), TokenType.SIGNUP)
    auth_service.verify_signup(str(token.token))
    result = auth_service.signin(data)
    assert result is not False
    assert result["session"] is not None
    assert result["session"]["token"] is not None
    assert result["session"]["expires_at"] is not None
    assert datetime.strptime(
        result["session"]["expires_at"], "%Y-%m-%d %H:%M:%S") > datetime.now()
    assert result["user"] is not None
    assert result["user"]["id"] is not None
    assert result["user"]["email"] == data["email"]
    assert result["user"]["name"] == data["name"]
    assert result["user"]["status"] == "ACTIVE"


def test_auth_signout():
    data = _prepare_user_data()
    auth_service.signup(data.copy())
    created_user = user_service.get_by_email(data["email"])
    token = verification_token_service.get_by_user_id(
        str(created_user.id), TokenType.SIGNUP)
    auth_service.verify_signup(str(token.token))
    signin_result = auth_service.signin(data)
    assert signin_result is not False
    session_token = signin_result["session"]["token"]
    signout_result = auth_service.signout(session_token)
    assert signout_result is True
    session = session_service.get_by_token(session_token)
    assert session is not None
    assert session.is_expired == True
    
def test_auth_forgot_password(mock_send_email):
    data = _prepare_user_data()
    auth_service.signup(data.copy())
    created_user = user_service.get_by_email(data["email"])
    token = verification_token_service.get_by_user_id(
        str(created_user.id), TokenType.SIGNUP)
    auth_service.verify_signup(str(token.token))
    mock_send_email.reset_mock()
    result = auth_service.forgot_password(data["email"])
    assert result is not False
    forgot_token = verification_token_service.get_by_user_id(
        str(created_user.id), TokenType.FORGOT)
    assert forgot_token is not None
    assert forgot_token.is_expired == False
    assert forgot_token.is_verified == False
    assert forgot_token.is_signup == False
    assert forgot_token.is_forgot == True
    mock_send_email.assert_called_once()
    
def test_auth_reset_password():
    data = _prepare_user_data()
    auth_service.signup(data.copy())
    created_user = user_service.get_by_email(data["email"])
    token = verification_token_service.get_by_user_id(
        str(created_user.id), TokenType.SIGNUP)
    auth_service.verify_signup(str(token.token))
    auth_service.forgot_password(data["email"])
    forgot_token = verification_token_service.get_by_user_id(
        str(created_user.id), TokenType.FORGOT)
    result = auth_service.reset_password(str(forgot_token.token), "newpassword")
    assert result is True
    verified_token = verification_token_service.get_by_user_id(
        str(created_user.id), TokenType.FORGOT)
    assert verified_token is not None
    assert verified_token.is_verified == True
    assert verified_token.is_expired == True
    old_password_signin_result = auth_service.signin(data)
    assert old_password_signin_result == False
    data["password"] = "newpassword"
    new_password_signin_result = auth_service.signin(data)
    assert new_password_signin_result is not False
    assert new_password_signin_result["session"] is not None
    assert new_password_signin_result["session"]["token"] is not None
    assert new_password_signin_result["session"]["expires_at"] is not None
    assert datetime.strptime(
        new_password_signin_result["session"]["expires_at"], "%Y-%m-%d %H:%M:%S") > datetime.now()
    
