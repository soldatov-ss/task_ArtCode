import asyncio
import json

import aiohttp
from django.shortcuts import render


async def get_response(session, url, params=None) -> json:
    headers = {'Accept-Language': 'ua'}
    if params:
        async with session.get(url, params=params) as res:
            return await res.json()
    async with session.get(url, headers=headers) as res:
        return await res.json()


async def index(request, *args, **kwargs):
    futures = []
    response_data = []

    urls = [
        'https://onboarding.art-code.team/api/test/v1/search/terms',
        'https://onboarding.art-code.team/api/test/v1/search/brands_terms',
        'https://onboarding.art-code.team/api/test/v1/search/styles'
    ]

    async with aiohttp.ClientSession() as session:
        for url in urls:
            futures.append(asyncio.ensure_future(get_response(session, url)))

        for res in await asyncio.gather(*futures):
            response_data.append(res)

    terms, brand_terms, styles = response_data
    context = {'terms': terms.get('data'), 'brand_terms': brand_terms.get('data'), 'styles': styles.get('data')}

    if kwargs:
        context['current_term'] = kwargs.get('service_slug')
        context['current_brand'] = kwargs.get('brand_slug')
        context['current_style'] = kwargs.get('style_slug')

        if len(kwargs) == 3:
            parse_url = 'https://onboarding.art-code.team/api/test/v1/search/parse_link'
            async with aiohttp.ClientSession() as session:
                parse_list = await get_response(session, parse_url, params=kwargs)

            context['parse_list'] = [parse_list]

    return render(request, 'swagger_app/index.html', context)
