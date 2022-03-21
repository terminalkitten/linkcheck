import httpx
from devtools import debug
from wasabi import Printer

msg = Printer()

# Async login for Django projects
async def login(username, password, settings):

    msg.divider(f"Start login for {username}")

    async with httpx.AsyncClient() as client:
        login_response = await client.get(
            f"{settings.hostname}/{settings.login_url_path}/"
        )
        csrftoken = login_response.cookies["csrftoken"]

    transport = httpx.AsyncHTTPTransport(retries=1)
    async with httpx.AsyncClient(
        transport=transport, cookies=login_response.cookies
    ) as client:
        try:
            auth_response = await client.post(
                f"{settings.hostname}/{settings.login_url_path}/?",
                data={
                    "username": username,
                    "password": password,
                    "csrfmiddlewaretoken": csrftoken,
                },
                headers={
                    "Host": f"{settings.hostname}",
                    "Origin": f"{settings.hostname}",
                    "Referer": f"{settings.hostname}/{settings.login_url_path}/",
                    "X-CSRFToken": csrftoken,
                },
            )
            msg.good(f"Success: got a cookie for {username}")
            return auth_response.cookies

        except Exception as e:
            debug(e)
