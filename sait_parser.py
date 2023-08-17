import asyncio, aiohttp
from bs4 import BeautifulSoup as bs
from aiogram.types import Message

headers= {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cookie':'BITRIX_SM_SALE_UID=354728472a78e7dc349a20c3ea70ddbe; PHPSESSID=d659d82bebfbe0633f0191eb1e064c59; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1692305940%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

async def parsing(session, link, message):
    async with session.get(link, headers=headers) as resp:
            if resp.status == 200:
                pass
            else:
                print(f'Ошибка: {resp.status}')
                asyncio.sleep(15)
            resp_text = await resp.text()
            soup = bs(resp_text, 'lxml')
            print(soup)
            items = soup.find_all('div', class_='product-block')

            for item in items:
                name = item.find('div', class_='name').text
                price = item.find('div', class_='price').find('span').text
                url = item.find('div', class_='name').find('a').get('href')
                url = 'https://www.hard-tuning.ru' + url

                name = name.replace('\t', '').replace('\n', '')
                name = name.replace('                                        ', '')

                export = f'''
Название: {name}
Цена: {price} рублей
Ссылка: {url}'''
                print(export)
                await message.answer(export)


async def start_parse(links, message: Message):
    async with aiohttp.ClientSession() as session:
        task = asyncio.create_task(parsing(session, links, message))
        await asyncio.gather(task)
    print('parsing...')


