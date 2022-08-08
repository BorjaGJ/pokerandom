import random

from django.shortcuts import render
from django.views.generic import CreateView
import pokepy

# Create your views here.


class Index(CreateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        cliente = pokepy.V2Client()
        oponent_party = []
        pokemon_party = get_random_pokemon_party(500, 600, cliente, 4)
        oponent_party2 = cliente.get_pokemon(550)
        oponent_party.append(oponent_party2)


        return render(request, self.template_name, {'pokemon_party': pokemon_party,
                                                    'oponent_party': oponent_party
                                                    })


def get_random_pokemon(start, end, cliente):

    number = random.randint(start, end)
    return cliente.get_pokemon(number)


def get_random_pokemon_party(start, end, cliente, x=1):

    pokemon_list = []

    if x > 6 or x < 1:
        raise ValueError('The party length must be between 1 and 6')

    for a in range(x):
        pokemon = get_random_pokemon(start, end, cliente)
        pokemon_list.append(pokemon)

    return pokemon_list


class EnterForm(CreateView):
    template_name = 'form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})