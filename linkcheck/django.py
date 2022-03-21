import httpx
from devtools import debug
from wasabi import Printer

msg = Printer()

# Async login for Django projects
async def login(username, password, config):

    msg.divider(f"Start login for {username}")

    async with httpx.AsyncClient() as client:
        login_response = await client.get(f"{config.hostname}/{config.login_url_path}/")
        csrftoken = login_response.cookies["csrftoken"]

    transport = httpx.AsyncHTTPTransport(retries=1)
    async with httpx.AsyncClient(
        transport=transport, cookies=login_response.cookies
    ) as client:
        try:
            auth_response = await client.post(
                f"{config.hostname}/{config.login_url_path}/?",
                data={
                    "username": username,
                    "password": password,
                    "csrfmiddlewaretoken": csrftoken,
                },
                headers={
                    "Host": f"{config.hostname}",
                    "Origin": f"{config.hostname}",
                    "Referer": f"{config.hostname}/{config.login_url_path}/",
                    "X-CSRFToken": csrftoken,
                },
            )
            msg.good(f"Success: got a cookie for {username}")
            return auth_response.cookies

        except Exception as e:
            debug(e)


async def run_link_checker(config):
    username, password = config.user.split(":")
    cookies = await login(username, password, config)
