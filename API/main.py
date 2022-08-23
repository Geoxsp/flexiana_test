import requests


class DeckApi:
    def __init__(self):
        self.base = "http://deckofcardsapi.com/api/deck/"

    def create_deck(self):
        return requests.get(self.base+"/new/")

    def shuffle_deck(self, deck_id, deck_count=1):
        return requests.get(self.base + f"{deck_id}/shuffle/?deck_count={deck_count}")

    def draw_cards_from_deck(self, deck_id, number_of_cards=1):
        return requests.get(self.base + f"{deck_id}/draw/?count={number_of_cards}")

    def add_to_pile(self, deck_id, pile_name, cards):
        return requests.get(self.base + f"{deck_id}/pile/{pile_name}/add/?cards={cards}")

    def read_from_pile(self, deck_id, pile_name):
        return requests.get(self.base + f"{deck_id}/pile/{pile_name}/list/")

    def shuffle_pile(self, deck_id, pile_name):
        return requests.get(self.base + f"{deck_id}/pile/{pile_name}/shuffle/")

    def draw_from_pile(self, deck_id, pile_name, count):
        return requests.get(self.base + f"{deck_id}/pile/{pile_name}/draw/?count={count}")
