from API.main import DeckApi
api = DeckApi()


# Create the deck
deck = api.create_deck()


# Create the deck tests
class TestDeck:
    def setup_method(self):
        self.deck = deck
        self.response = self.deck.json()

    def test_create_deck_status(self):
        assert self.deck.status_code == 200

    def test_deck_status(self):
        assert self.response["success"] is True

    def test_deck_remaining(self):
        assert self.response["remaining"] == 52

    def test_deck_shuffled(self):
        assert self.response["shuffled"] is False

    def test_has_id(self):
        assert "deck_id" in self.response


deck_id = deck.json()["deck_id"]
# Shuffle the deck
shuffled_deck = api.shuffle_deck(deck_id)


# Shuffle the deck tests
class TestShuffleDeck:
    def setup_method(self):
        self.deck = api.create_deck()
        self.deck_id = self.deck.json()['deck_id']
        self.shuffled_deck = api.shuffle_deck(self.deck_id)
        self.response = self.shuffled_deck.json()

    def test_status(self):
        assert self.shuffled_deck.status_code == 200, self.shuffled_deck.status_code

    def test_deck_status(self):
        assert self.response["success"] is True

    def test_deck_remaining(self):
        assert self.response["remaining"] == 52

    def test_deck_shuffled(self):
        assert self.response["shuffled"] is True

    def test_has_id(self):
        assert "deck_id" in self.response


# Draw 3 cards from deck
draw_cards = api.draw_cards_from_deck(deck_id, 3)


# Draw 3 cards from deck test
class TestDrawCards:
    def setup_method(self):
        self.deck = api.create_deck()
        self.deck_id = self.deck.json()['deck_id']
        self.draw_cards = api.draw_cards_from_deck(self.deck_id, 3)
        self.response = self.draw_cards.json()

    def test_status(self):
        assert self.draw_cards.status_code == 200

    def test_deck_status(self):
        assert self.response["success"] is True

    def test_deck_remaining(self):
        assert self.response["remaining"] == 52 - 3

    def test_has_id(self):
        assert "deck_id" in self.response

    def test_got_cards(self):
        assert len(self.response['cards']) == 3

    def test_cards_have_code(self):
        for card in self.response['cards']:
            assert "code" in card, f"{card} has no code"

    def test_cards_have_image(self):
        for card in self.response['cards']:
            assert "image" in card, f"{card} has no image"

    def test_cards_have_value(self):
        for card in self.response['cards']:
            assert "value" in card, f"{card} has no value"

    def test_cards_have_suite(self):
        for card in self.response['cards']:
            assert "suit" in card, f"{card} has no suit"


# Make 2 piles with 5 cards each from deck
draw_cards_for_pile1 = api.draw_cards_from_deck(deck_id, 5).json()['cards']
draw_cards_for_pile2 = api.draw_cards_from_deck(deck_id, 5).json()['cards']


cards_p1 = ",".join([card['code'] for card in draw_cards_for_pile1])
cards_p2 = ",".join([card['code'] for card in draw_cards_for_pile2])
pile_1 = api.add_to_pile(deck_id, "pile1", cards_p1)
pile_2 = api.add_to_pile(deck_id, "pile2", cards_p2)


class TestPile:
    def setup_method(self):
        self.deck = api.create_deck()
        self.deck_id = self.deck.json()["deck_id"]
        self.cards_fp1 = api.draw_cards_from_deck(self.deck_id, 5).json()['cards']
        self.cards_p1 = ",".join([card['code'] for card in self.cards_fp1])
        self.pile = api.add_to_pile(self.deck_id, "pile1", self.cards_p1)
        self.response = self.pile.json()

    def test_status(self):
        assert self.pile.status_code == 200

    def test_pile_status(self):
        assert self.response["success"] is True

    def test_pile_remaining(self):
        assert self.response["remaining"] == 47

    def test_has_id(self):
        assert "deck_id" in self.response

    def test_has_pile(self):
        assert "piles" in self.response

    def test_pile_name(self):
        assert "pile1" in self.response['piles']


# List the cards in pile1 and pile2 test
read_pile1 = api.read_from_pile(deck_id, "pile1")
read_pile2 = api.read_from_pile(deck_id, "pile2")


class TestReadPile:
    def setup_method(self):
        self.deck = api.create_deck()
        self.deck_id = self.deck.json()["deck_id"]
        self.cards_fp1 = api.draw_cards_from_deck(self.deck_id, 5).json()['cards']
        self.cards_p1 = ",".join([card['code'] for card in self.cards_fp1])
        self.pile = api.add_to_pile(self.deck_id, "pile1", self.cards_p1).json()
        self.read_pile = api.read_from_pile(self.deck_id, "pile1")
        self.response = self.read_pile.json()

    def test_status(self):
        assert self.read_pile.status_code == 200

    def test_deck_status(self):
        assert self.response["success"] is True

    def test_deck_remaining(self):
        assert self.response["remaining"] == 47

    def test_has_id(self):
        assert "deck_id" in self.response

    def test_piles_have_cards(self):
        for pile, details in self.response['piles'].items():
            if pile == "pile1":
                assert "cards" in details, details

    def test_piles_have_count(self):
        for pile, details in self.response['piles'].items():
            assert "remaining" in details, f"{pile} has no remaining"

    def test_pile_cards_have_code(self):
        for pile, details in self.response['piles'].items():
            if pile == "pile1":
                for card in details['cards']:
                    assert "code" in card, f"{card} has no code"

    def test_pile_cards_have_image(self):
        for pile, details in self.response['piles'].items():
            if pile == "pile1":
                for card in details['cards']:
                    assert "code" in card, f"{card} has no image"

    def test_pile_cards_have_value(self):
        for pile, details in self.response['piles'].items():
            if pile == "pile1":
                for card in details['cards']:
                    assert "value" in card, f"{card} has no value"

    def test_pile_cards_have_suite(self):
        for pile, details in self.response['piles'].items():
            if pile == "pile1":
                for card in details['cards']:
                    assert "suit" in card, f"{card} has no suit"


# List the cards in pile1 and pile2
pile_1_cards = read_pile1.json()['piles']['pile1']['cards']
pile_2_cards = read_pile2.json()['piles']['pile2']['cards']
print(pile_1_cards)
print(pile_2_cards)


# shuffle pile1

shuffled_pile_1 = api.shuffle_pile(deck_id, "pile1")


class TestShufflePile:
    def setup_method(self):
        self.deck = api.create_deck()
        self.deck_id = self.deck.json()["deck_id"]
        self.cards_fp1 = api.draw_cards_from_deck(self.deck_id, 5).json()['cards']
        self.cards_p1 = ",".join([card['code'] for card in self.cards_fp1])
        self.pile = api.add_to_pile(self.deck_id, "pile1", self.cards_p1).json()
        self.shuffle_pile = api.shuffle_pile(self.deck_id, "pile1")
        self.response = self.shuffle_pile.json()

    def test_status(self):
        assert self.shuffle_pile.status_code == 200

    def test_deck_status(self):
        assert self.response["success"] is True

    def test_deck_remaining(self):
        assert self.response["remaining"] == 47

    def test_has_id(self):
        assert "deck_id" in self.response

    def test_has_piles(self):
        assert "piles" in self.response


# Read pile1 again and compare cards before and after shuffling
shuffled_pile_1_cards = api.read_from_pile(deck_id, "pile1").json()['piles']['pile1']['cards']


def test_pile_shuffle():
    assert pile_1_cards != shuffled_pile_1_cards


class TestDrawFromPile:
    def setup_method(self):
        self.deck = api.create_deck()
        self.deck_id = self.deck.json()["deck_id"]
        self.cards_fp1 = api.draw_cards_from_deck(self.deck_id, 5).json()['cards']
        self.cards_p1 = ",".join([card['code'] for card in self.cards_fp1])
        api.add_to_pile(self.deck_id, "pile1", self.cards_p1).json()
        self.draw = api.draw_from_pile(self.deck_id, "pile1", 1)
        self.response = self.draw.json()

    def test_status(self):
        assert self.draw.status_code == 200

    def test_deck_status(self):
        assert self.response["success"] is True

    def test_has_id(self):
        assert "deck_id" in self.response

    def test_got_cards(self):
        print(self.response)
        assert len(self.response['cards']) == 1, self.response

    def test_cards_have_code(self):
        print(self.response)
        for card in self.response['cards']:
            assert "code" in card, f"{card} has no code"

    def test_cards_have_image(self):
        print(self.response)
        for card in self.response['cards']:
            assert "image" in card, f"{card} has no image"

    def test_cards_have_value(self):
        for card in self.response['cards']:
            assert "value" in card, f"{card} has no value"

    def test_cards_have_suite(self):
        for card in self.response['cards']:
            assert "suit" in card, f"{card} has no suit"


# draw 2 cards from pile1
draw_pile_1 = api.draw_from_pile(deck_id, "pile1", 2)

# draw 3 cards from pile2
draw_pile_2 = api.draw_from_pile(deck_id, "pile2", 3)

