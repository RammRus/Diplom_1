import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient

#Тест на метод set_buns()
def test_set_buns():
    mock_bun = Mock(spec=Bun)
    mock_bun.get_name.return_value = "MockBun"
    mock_bun.get_price.return_value = 1.5
    burger = Burger()
    burger.set_buns(mock_bun)
    assert burger.bun.get_name() == "MockBun"
    assert burger.bun.get_price() == 1.5


#Тест на метод add_ingredient()
@pytest.mark.parametrize("name, type_, price", [
    ("Lettuce", "FILLING", 0.5),
    ("Ketchup", "SAUCE", 0.2)
])
def test_add_ingredient(name, type_, price):
    mock_ing = Mock(spec=Ingredient)
    mock_ing.get_name.return_value = name
    mock_ing.get_type.return_value = type_
    mock_ing.get_price.return_value = price

    burger = Burger()
    burger.add_ingredient(mock_ing)
    assert burger.ingredients[-1].get_name() == name
    assert burger.ingredients[-1].get_type() == type_

#Тест на метод remove_ingredient()
def test_remove_ingredient():
    ing1 = Ingredient("FILLING", "Lettuce", 0.5)
    ing2 = Ingredient("SAUCE", "Ketchup", 0.2)

    burger = Burger()

    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)
    burger.remove_ingredient(0)
    assert burger.ingredients == [ing2]

#Тест на метод move_ingredients
@pytest.mark.parametrize("from_idx, to_idx", [
    (0, 1)
])
def test_move_ingredients(from_idx, to_idx):
    ing1 = Mock(spec=Ingredient)
    ing1.get_name.return_value = "Lettuce"

    ing2 = Mock(spec=Ingredient)
    ing2.get_name.return_value = "Ketchup"

    burger = Burger()
    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)
    ing_to_move = burger.ingredients[from_idx]
    burger.move_ingredient(from_idx, to_idx)
    assert burger.ingredients[to_idx].get_name() == ing_to_move.get_name()

#Тест на метод get_price()
@pytest.mark.parametrize("bun_name, bun_price, ing_name, ing_price", [
    ("Brioche", 1.8, "Lettuce", 0.5),
    ("WholeWheat", 2.0, "Ketchup", 0.2)
])
def test_get_price(bun_name, bun_price, ing_name, ing_price):
    mock_bun = Mock(spec=Bun)
    mock_bun.get_name.return_value = bun_name
    mock_bun.get_price.return_value = bun_price
    mock_ing = Mock(spec=Ingredient)
    mock_ing.get_name.return_value = ing_name
    mock_ing.get_price.return_value = ing_price
    mock_ing.get_type.return_value = "FILLING"

    burger = Burger()
    burger.set_buns(mock_bun)
    burger.add_ingredient(mock_ing)
    expected_price = 2*bun_price+ing_price
    actual_price = burger.get_price()
    assert expected_price == actual_price

#Тест на метод get_receipe()
def test_get_receipt():
    mock_bun = Mock(spec=Bun)
    mock_bun.get_name.return_value = "Sesame"
    mock_bun.get_price.return_value = 1.2

    mock_ing1 = Mock(spec=Ingredient)
    mock_ing1.get_name.return_value = "Cheese"
    mock_ing1.get_type.return_value = "FILLING"
    mock_ing1.get_price.return_value = 0.5

    mock_ing2 = Mock(spec=Ingredient)
    mock_ing2.get_name.return_value = "Kethcup"
    mock_ing2.get_type.return_value = "SAUCE"
    mock_ing2.get_price.return_value = 0.2

    burger = Burger()
    burger.set_buns(mock_bun)
    burger.add_ingredient(mock_ing1)
    burger.add_ingredient(mock_ing2)
    receipt = burger.get_receipt()
    total_price = burger.get_price()

    assert f"(==== {mock_bun.get_name()} ====)" in receipt
    assert f"= {mock_ing1.get_type().lower()} {mock_ing1.get_name()} =" in receipt
    assert f"= {mock_ing2.get_type().lower()} {mock_ing2.get_name()} =" in receipt
    assert f"Price: {total_price}" in receipt