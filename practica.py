"""Converting database rows to public API objects."""

from datetime import datetime
from typing import Any


def _get(row: Any, name: str) -> Any:
  """Read a field from either a mapping or an object."""
  if isinstance(row, dict):
    return row.get(name)
  return getattr(row, name, None)


def _iso(value: Any) -> Any:
  return value.isoformat() if isinstance(value, datetime) else value


def _money(value: Any) -> Any:
  return round(float(value), 2) if value is not None else value


def to_public_user(row: Any) -> dict[str, Any]:
  return {
    "id": _get(row, "id"),
    "name": _get(row, "name"),
    "email": _get(row, "email"),
    "role": _get(row, "role"),
    "isActive": _get(row, "isActive"),
  }


def to_category(row: Any) -> dict[str, Any]:
  return {
    "id": _get(row, "id"),
    "name": _get(row, "name"),
    "description": _get(row, "description"),
    "createdAt": _iso(_get(row, "createdAt")),
    "updatedAt": _iso(_get(row, "updatedAt")),
  }


def to_product(row: Any) -> dict[str, Any]:
  result = {name: _get(row, name) for name in (
    "id", "sku", "name", "description", "categoryId", "stock",
    "minStock", "isActive",
  )}
  result.update({
    "price": _money(_get(row, "price")),
    "cost": _money(_get(row, "cost")),
    "createdAt": _iso(_get(row, "createdAt")),
    "updatedAt": _iso(_get(row, "updatedAt")),
  })
  return result


def to_sale(row: Any) -> dict[str, Any]:
  result = {name: _get(row, name) for name in (
    "id", "code", "userId", "customerName", "customerDocument",
    "paymentMethod", "status",
  )}
  result.update({name: _money(_get(row, name)) for name in (
    "subtotal", "discount", "tax", "total",
  )})
  result["createdAt"] = _iso(_get(row, "createdAt"))
  return result


def to_sale_item(row: Any) -> dict[str, Any]:
  result = {name: _get(row, name) for name in (
    "id", "saleId", "productId", "productName", "quantity",
  )}
  result.update({name: _money(_get(row, name)) for name in ("unitPrice", "subtotal")})
  return result


def to_stock_movement(row: Any) -> dict[str, Any]:
  result = {name: _get(row, name) for name in (
    "id", "productId", "type", "quantity", "previousStock",
    "newStock", "reason", "saleId", "userId",
  )}
  result["createdAt"] = _iso(_get(row, "createdAt"))
  return result
