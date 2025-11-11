from starlette.testclient import TestClient

from storytime import make_site
from storytime.app import create_app


def test_application(tmp_path):
    site = make_site("storytime")
    app = create_app(site)
    client = TestClient(app)
    response = client.get("/stories/about/company/me/")
    assert response.status_code == 200
    assert response.text == "Full path: about/company/me"
