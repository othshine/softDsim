from django.db import models

from app.models.decision_models.decision_model import Decision


class TextBlock(models.Model):

    id = models.AutoField(primary_key=True)
    header = models.TextField()
    content = models.TextField()

    decision = models.ForeignKey(
        Decision,
        on_delete=models.CASCADE,
        related_name="text_block",
        blank=True,
        null=True,
    )


# def create(self, validated_data):
#     request_orders_data = validated_data.pop(‘request_orders’)
#     request = Request.objects.create(**validated_data)
#
#     for request_order_data in request_orders_data:
#         ro_items = request_order_data.pop(‘request_order_itemss’)
#         order = RequestOrders.objects.create(request_id=request, **request_order_data)
#         for ro_item in ro_items:
#             RequestOrderItemss.create(request_order_id=order, **ro_item)
#     return request
