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
        your_party = int(request.POST['yourparty'])
        rival_party = int(request.POST['rivalparty'])
        start_pokemon = get_gen_range(request.POST['firstgen'])[0]
        end_pokemon = get_gen_range(request.POST['secondgen'])[1]

        return redirect('battle', start_pokemon, end_pokemon, your_party, rival_party)


class Battle(CreateView):
    template_name = 'battle.html'

    def get(self, request, *args, **kwargs):
        cliente = pokepy.V2Client()

        pokemon_party = get_random_pokemon_party(int(self.kwargs['startpokemon']), int(self.kwargs['endpokemon']),
                                                 cliente, int(self.kwargs['yourparty']))

        oponent_party = get_random_pokemon_party(int(self.kwargs['startpokemon']), int(self.kwargs['endpokemon']),
                                                 cliente, int(self.kwargs['rivalparty']))

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
