import asyncio
import logging
from datetime import datetime, timedelta

import json
import aiohttp
import names
import aiofile
import aiopath
import websockets
from websockets.exceptions import ConnectionClosedOK
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)


class ExchangeRates:

    URL = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5&date="

    def __init__(self, currency_codes):
        self.currency_codes = currency_codes
        self.session = None

    async def create_session(self):
        self.session = aiohttp.ClientSession()

    async def bound_fetch(self, url):
        async with self.session.get(url) as response:
            if response.status != 200:
                raise ValueError(
                    f"Status code {response.status}")
            return await response.text()

    async def get_rates(self, days=1):
        today = datetime.now()
        date_range = [today - timedelta(days=x) for x in range(days)]
        result = ""
        for date in date_range:
            url = f"{self.URL}{date.strftime('%d.%m.%Y')}"
            response_text = await self.bound_fetch(url)
            response_json = json.loads(response_text)
            for currency in response_json:
                if currency['ccy'] in self.currency_codes:
                    result += (
                       f"{date:%d.%m.%Y}, Course {currency['ccy']}:\nSelling {currency['sale']}, Buy {currency['buy']}\n"
                    )
        return result

    async def close(self):
        await self.session.close()


class Server:
    
    clients = set()
    currency_codes = ['USD', 'EUR']
    exchange_rates = ExchangeRates(currency_codes)

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.lower().startswith("exchange"):
                try:
                    days = int(message.split()[1])
                except:
                    days = 1
                result = await self.exchange_rates.get_rates(days)
                await self.send_to_clients(result)

                async with aiofile.async_open(aiopath.Path(__file__).parent / "chat.log", mode="a") as f:
                    await f.write(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}:\n{result}\n')
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    await server.exchange_rates.create_session()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())