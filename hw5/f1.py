import requests
import click


currencies = requests.get('http://www.nbrb.by/API/ExRates/Currencies').json()


@click.command()
@click.argument('currency')
def get_rate(currency):
    cur = list(filter(lambda x: x['Cur_Abbreviation'] == currency, currencies))
    if cur:
        currency_id = cur[-1]['Cur_ID']
    else:
        click.echo(f'There is no such currency with code {currency}')
        return
    r = requests.get(f'http://www.nbrb.by/API/ExRates/Rates/{currency_id}')
    if r.status_code == requests.codes.ok:
        rate = r.json()
        click.echo(f"1 BYN = {round(rate['Cur_Scale'] / rate['Cur_OfficialRate'], 2)} {currency}")
    else:
        click.echo(f'Unable to get currency. Status code: {r.status_code}')


if __name__ == "__main__":
    get_rate()
