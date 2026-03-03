import pytest
from unittest.mock import Mock

from burger import Burger


class TestBurger:

    def test_set_buns(self):
        burger = Burger()
        bun = Mock()
        burger.set_buns(bun)
        assert burger.bun == bun

    def test_add_ingredient(self):
        burger = Burger()
        ingredient = Mock()
        burger.add_ingredient(ingredient)
        assert ingredient in burger.ingredients

    def test_remove_ingredient(self):
        burger = Burger()
        ingredient = Mock()
        burger.add_ingredient(ingredient)
        burger.remove_ingredient(0)
        assert burger.ingredients == []

    def test_move_ingredient(self):
        burger = Burger()
        ing1, ing2 = Mock(), Mock()
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.move_ingredient(0, 1)
        assert burger.ingredients == [ing2, ing1]

    @pytest.mark.parametrize(
        "bun_price, ingredient_prices, expected",
        [
            (100, [], 200),
            (100, [50], 250),
            (100, [50, 25], 275),
        ],
    )
    def test_get_price(self, bun_price, ingredient_prices, expected):
        burger = Burger()

        bun = Mock()
        bun.get_price.return_value = bun_price
        burger.set_buns(bun)

        for p in ingredient_prices:
            ing = Mock()
            ing.get_price.return_value = p
            burger.add_ingredient(ing)

        assert burger.get_price() == expected

    def test_get_receipt_contains_names_and_price(self):
        burger = Burger()

        bun = Mock()
        bun.get_name.return_value = "Булка"
        bun.get_price.return_value = 100
        burger.set_buns(bun)

        ing = Mock()
        ing.get_name.return_value = "Сыр"
        ing.get_price.return_value = 50
        ing.get_type.return_value = "FILLING"
        burger.add_ingredient(ing)

        receipt = burger.get_receipt()
        assert "Булка" in receipt
        assert "Сыр" in receipt
        assert "Price:" in receipt
        assert "250" in receipt
        