import pytest
import os
from services.captcha import generate_captcha, verify_captcha, generate_captcha_url
from unittest.mock import patch

@pytest.fixture
def setup_captcha():
    os.makedirs("assets/captcha_images", exist_ok=True)
    with open("assets/captcha_images/test.png", "wb") as f:
        f.write(b"mock_image_data")

def test_captcha_generation(setup_captcha):
    user_id = 123
    image_path, code = generate_captcha(user_id)
    assert os.path.exists(image_path)
    assert len(code) == 6
    assert verify_captcha(user_id, code) == True
    assert verify_captcha(user_id, "wrong") == False
    assert verify_captcha(user_id, code) == False  # Expired after verification

def test_captcha_url(setup_captcha):
    with patch("services.captcha.BASE_URL", "https://test.com"):
        user_id = 123
        url = generate_captcha_url(user_id)
        assert url.startswith("https://test.com/captcha/123/")
