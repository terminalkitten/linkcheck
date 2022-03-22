from contextlib import contextmanager
from typing import Optional, Any
import asyncio
from bs4.element import ResultSet

import httpx
from bs4 import BeautifulSoup
from devtools import debug
from httpx import Cookies
from playwright.async_api import async_playwright
from wasabi import Printer

from yaspin import yaspin
from yaspin.spinners import Spinners

from linkcheck import __version__ as VERSION

msg = Printer()

# Link caches
URL_CACHE = set()
BROWSER_URL_CACHE = set()

# Context helper for users defined in TOML file
@contextmanager
def config_users(config):
    for auth in config.users:
        yield auth.split(":")


# Async login for Django projects
async def login(username, password, config) -> Optional[Cookies]:
    async with httpx.AsyncClient() as client:
        login_response = await client.get(f"{config.hostname}/{config.login_url_path}/")
        csrftoken = login_response.cookies["csrftoken"]

    transport = httpx.AsyncHTTPTransport(retries=1)
    async with httpx.AsyncClient(
        transport=transport, cookies=login_response.cookies
    ) as client:
        try:
            login_url = f"{config.hostname}/{config.login_url_path}/"
            auth_response = await client.post(
                login_url,
                data={
                    "username": username,
                    "password": password,
                    "csrfmiddlewaretoken": csrftoken,
                },
                headers={
                    "User-Agent": f"Django LinkCheck / {VERSION}",
                    "Host": f"localhost",  # FIXME - Extract hostname without port from hostname
                    "Origin": f"{config.hostname}",
                    "Referer": f"{config.hostname}/{config.login_url_path}/",
                    "X-CSRFToken": csrftoken,
                },
            )
            msg.good(f"Success: got a cookie for {username}")

            return auth_response.cookies

        except Exception as e:
            debug(e)


async def extract_href(text) -> ResultSet[Any]:
    soup = BeautifulSoup(text, features="html.parser")
    return soup.find_all(href=True)


async def visit_link(url, cookies, config) -> None:
    await asyncio.sleep(0.9)

    if url in URL_CACHE:
        return None

    URL_CACHE.add(url)
    with yaspin(Spinners.arc, text=url) as status:
        try:
            async with httpx.AsyncClient(
                cookies=cookies, follow_redirects=True
            ) as client:
                response = await client.get(
                    url,
                    headers={"User-Agent": f"Django LinkCheck / {VERSION}"},
                )
                href_tags = await extract_href(response.text)
                for href in href_tags:
                    if href["href"].startswith("/"):
                        url_from_href = config.hostname + href["href"]
                        status.text = f"[scrape] {url_from_href}"
                        await visit_link(url_from_href, cookies, config)

        except Exception as e:
            debug(e)


async def get_hrefs(page):
    return await page.eval_on_selector_all(
        "[href^='/']", "elements => elements.map(element => element.href)"
    )


async def browse_link(url, page, config) -> None:
    BROWSER_URL_CACHE.add(url)

    try:
        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        hrefs_on_page = await get_hrefs(page)
        if hrefs_on_page:
            new_urls = set(hrefs_on_page).difference(BROWSER_URL_CACHE)
            BROWSER_URL_CACHE.update(hrefs_on_page)
            for link in new_urls:
                await browse_link(link, page, config)

    except Exception as e:
        debug(e)


async def link_checker_visit(config):
    for auth in config.users:
        username, password = auth.split(":")
        cookies = await login(username, password, config)
        await visit_link(config.hostname + config.entry_point, cookies, config)


async def link_checker_browser(config):
    with config_users(config) as auth:
        username, password = auth
        playwright_cookies = []
        cookies = await login(username, password, config)
        if cookies:
            for key in cookies.keys():
                playwright_cookies.append(
                    {"name": key, "value": cookies.get(key), "url": config.hostname}
                )

            async with async_playwright() as p:
                browser = await p.chromium.launch()
                context = await browser.new_context()
                page = await context.new_page()

                await context.add_cookies(playwright_cookies)
                await browse_link(config.hostname + config.entry_point, page, config)
                await browser.close()
