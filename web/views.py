import random

from django.shortcuts import render, redirect
from django.views.generic import CreateView
import pokepy


# Create your views here.

class Index(CreateView):
    template_name = 'form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        your_party_size = int(request.POST['yourparty'])
        rival_party_size = int(request.POST['rivalparty'])
        start_pokemon = get_gen_range(request.POST['firstgen'])[0]
        end_pokemon = get_gen_range(request.POST['secondgen'])[1]

        request.session['legend'] = False
        request.session['mythic'] = False
        request.session['additems'] = False

        if 'banlegend' in request.POST:
            request.session['legend'] = True

        if 'banmythic' in request.POST:
            request.session['mythic'] = True

        if 'additems' in request.POST:
            request.session['additems'] = True

        return redirect('battle', start_pokemon, end_pokemon, your_party_size, rival_party_size)


class Battle(CreateView):
    template_name = 'battle.html'

    def get(self, request, *args, **kwargs):
        cliente = pokepy.V2Client()

        pokemon_party = get_random_pokemon_party(int(self.kwargs['startpokemon']), int(self.kwargs['endpokemon']),
                                                 cliente, int(self.kwargs['yourparty']))

        oponent_party = get_random_pokemon_party(int(self.kwargs['startpokemon']), int(self.kwargs['endpokemon']),
                                                 cliente, int(self.kwargs['rivalparty']))

        if request.session['legend']:
            pokemon_party = ban_legendaries(pokemon_party,
                                            int(self.kwargs['startpokemon']), int(self.kwargs['endpokemon']), cliente)

            oponent_party = ban_legendaries(oponent_party,
                                            int(self.kwargs['startpokemon']), int(self.kwargs['endpokemon']), cliente)

        if request.session['mythic']:
            pokemon_party = ban_mythics(pokemon_party,
                                            int(self.kwargs['startpokemon']), int(self.kwargs['endpokemon']), cliente)

            oponent_party = ban_mythics(oponent_party,
                                            int(self.kwargs['startpokemon']), int(self.kwargs['endpokemon']), cliente)

        your_items = []
        oponent_items = []

        if request.session['additems']:

            for pokemon in pokemon_party:
                item = get_random_item(cliente)
                your_items.append(item)

            for pokemon in oponent_party:
                item = get_random_item(cliente)
                oponent_items.append(item)

        return render(request, self.template_name, {'pokemon_party': pokemon_party,
                                                    'oponent_party': oponent_party,
                                                    'your_items': your_items,
                                                    'oponent_items': oponent_items,
                                                    })


def get_random_pokemon(start, end, cliente):
    number = random.randint(start, end)
    return cliente.get_pokemon(number)


def get_random_pokemon_species(start, end, cliente):
    number = random.randint(start, end)
    return cliente.get_pokemon_species(number)


def get_random_pokemon_party(start, end, cliente, x=1):
    pokemon_list = []

    if x > 6 or x < 1:
        raise ValueError('The party length must be between 1 and 6')

    for a in range(x):
        pokemon = get_random_pokemon(start, end, cliente)
        pokemon_list.append(pokemon)

    return pokemon_list


def get_gen_range(gen):
    range_dict = {
        '1': [1, 151],
        '2': [152, 251],
        '3': [252, 386],
        '4': [387, 493],
        '5': [494, 649],
        '6': [650, 721],
        '7': [722, 809],
        '8': [810, 898]
    }

    if int(gen) > 8 or int(gen) < 1:
        raise ValueError('must be between 1 and 8')

    return range_dict[gen]


def ban_legendaries(pokemon_party, start, end, cliente):

    final_party = []

    legendaries = [
        "articuno", "zapdos", "moltres", "mewtwo", "raikou", "entei", "lugia", "ho-oh",
        "suicune", "regirock", "regice", "registeel", "latias", "latios", "kyogre", "groudon", "rayquaza",
        "uxie", "mesprit", "azelf", "dialga", "palkia", "heatran", "regigigas	", "giratina", "cresselia",
        "cobalion", "terrakion", "virizion", "tornadus", "thundurus", "reshiram", "zekrom", "landorus", "kyurem",
        "xerneas", "yveltal", "zygarde", "necrozma", "solgaleo", "lunala", "tapu-Koko",
        "tapu-Fini", "tapu-Lele", "tapu-Bulu", "silvally", "zacian", "zamazenta",
        "eternatus", "urshifu", "calyrex", "glastrier", "spectrier", "regidrago", "regieleki"

    ]


    for pokemon in pokemon_party:

        if pokemon.name in legendaries:

            pokemon = get_random_pokemon(start, end, cliente)

            if pokemon.name in legendaries:
                pokemon = cliente.get_pokemon(468)


            final_party.append(pokemon)


        else:
            final_party.append(pokemon)


    return final_party




def ban_mythics(pokemon_party, start, end, cliente):

    final_party = []

    mythics = [
        "new", "celebi", "jirachi", "manaphy", "darkrai", "shaymin", "arceus", "victini", "deoxys", "keldeo",
        "meloetta", "genesect", "diancie", "hoopa", "volcanion", "magearna", "marshadow", "zeraora", "zarude",
        "meltan", "melmetal"
        ]

    extra = ["Phione", "Cubfoo", "Code cero", "cosmog", "cosmoem"]

    for pokemon in pokemon_party:

        if pokemon.name in mythics:

            pokemon = get_random_pokemon(start, end, cliente)

            if pokemon.name in mythics:
                pokemon = cliente.get_pokemon(468)

            final_party.append(pokemon)


        else:
            final_party.append(pokemon)

    return final_party


def get_random_item(cliente):

    items = cliente.get_item_category(12)

    number = random.randint(0, 60)

    item = items.items[number]

    return item