from api.operations.models import Product


def get_values(data, keys):
    result = {}
    if isinstance(data, dict) and 'products' in data:
        products = data['products']
        for product in products:
            for key in keys:
                if key in product:
                    result[key] = product[key]
    elif isinstance(data, list):
        for item in data:
            result.update(get_values(item, keys))
    return result


def create_object(artikul, ready_data):
    if 'name' not in ready_data:
        raise ValueError(f"товара с articul: {artikul} не существует")
    product = Product(
        articul=artikul,
        name=ready_data['name'],
        price=ready_data['priceU'],
        rating=ready_data['rating'],
        total_quantity=ready_data['totalQuantity']
    )
    return product


async def pars_wb(artikul, httpxclient):
    response = await httpxclient.get(
        f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}")
    data = response.json()
    return data
