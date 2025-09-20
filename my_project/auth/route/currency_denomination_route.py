# currency_denominations_routes.py
from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller.currency_denomination_controller import CurrencyDenominationsController
from my_project.auth.domain.orders.CurrecyDenomination import CurrencyDenominations

currency_denominations_bp = Blueprint('currency_denominations', __name__, url_prefix='/currency_denominations')
controller = CurrencyDenominationsController()
@currency_denominations_bp.get('')
def get_all_currency_denominations() -> Response:
    """
    ---
    summary: Отримати всі валютні номінали
    description: Повертає список усіх доступних валютних номіналів.
    responses:
      200:
        description: Успішне отримання списку валютних номіналів
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  value:
                    type: number
    """
    denominations = controller.find_all()
    dto = [cd.put_into_dto() for cd in denominations]
    return make_response(jsonify(dto), HTTPStatus.OK)


@currency_denominations_bp.post('')
def create_currency_denomination() -> Response:
    """
    ---
    summary: Створити новий валютний номінал
    description: Додає новий валютний номінал у систему.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              value:
                type: number
    responses:
      201:
        description: Валютний номінал успішно створено
    """
    content = request.get_json()
    denomination = CurrencyDenominations.create_from_dto(content)
    controller.create(denomination)
    return make_response(jsonify(denomination.put_into_dto()), HTTPStatus.CREATED)


@currency_denominations_bp.get('/<int:id>')
def get_currency_denomination(id: int) -> Response:
    """
    ---
    summary: Отримати валютний номінал за ID
    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Ідентифікатор валютного номіналу
    responses:
      200:
        description: Успішне отримання валютного номіналу
      404:
        description: Валютний номінал не знайдено
    """
    denomination = controller.find_by_id(id)
    if denomination:
        return make_response(jsonify(denomination.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Currency Denomination not found"}), HTTPStatus.NOT_FOUND)


@currency_denominations_bp.put('/<int:id>')
def update_currency_denomination(id: int) -> Response:
    """
    ---
    summary: Оновити валютний номінал
    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Ідентифікатор валютного номіналу
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              value:
                type: number
    responses:
      200:
        description: Валютний номінал успішно оновлено
      404:
        description: Валютний номінал не знайдено
    """
    content = request.get_json()
    denomination = CurrencyDenominations.create_from_dto(content)
    controller.update(id, denomination)
    return make_response("Currency Denomination updated", HTTPStatus.OK)


@currency_denominations_bp.delete('/<int:id>')
def delete_currency_denomination(id: int) -> Response:
    """
    ---
    summary: Видалити валютний номінал
    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Ідентифікатор валютного номіналу
    responses:
      204:
        description: Валютний номінал успішно видалено
      404:
        description: Валютний номінал не знайдено
    """
    controller.delete(id)
    return make_response("Currency Denomination deleted", HTTPStatus.NO_CONTENT)
