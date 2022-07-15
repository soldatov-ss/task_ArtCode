import asyncio

import aiohttp
from django.shortcuts import render


async def get_response(session, url):
    headers = {'Accept-Language': 'ua'}
    async with session.get(url, headers=headers) as res:
        return await res.json()


async def index(request, *args, **kwargs):
    futures = []
    response_data = []

    urls = [
        'https://autobooking.com/api/test/v1/search/terms',
        'https://autobooking.com/api/test/v1/search/brands_terms',

        # 'https://autobooking.com/api/test/v1/search/styles'
    ]

    async with aiohttp.ClientSession() as session:
        for url in urls:
            futures.append(asyncio.ensure_future(get_response(session, url)))

        for res in await asyncio.gather(*futures):
            response_data.append(res)

    # terms, brand_terms, styles = response_data
    terms, brand_terms = response_data

    styles = ['something1', 'something2', 'something3', 'something4', 'something5', ]

    # context = {'terms': terms.get('data'), 'brand_terms': brand_terms.get('data'), 'styles': styles.get('data')}
    context = {'terms': terms.get('data'), 'brand_terms': brand_terms.get('data'), 'styles': styles}

    if kwargs:
        context['current_term'] = kwargs.get('service_slug')
        context['current_brand'] = kwargs.get('brand_slug')
        context['current_style'] = kwargs.get('style_slug')
    return render(request, 'swagger_app/index.html', context)
