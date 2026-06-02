from flask import Blueprint, jsonify
from ..models.models import Order

billing_bp = Blueprint("billing_bp", __name__, url_prefix="/api/orders")

@billing_bp.route("/", methods=["GET"])
def list_orders():
    """List all processed orders"""
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders]), 200