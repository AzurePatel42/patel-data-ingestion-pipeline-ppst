from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)



class EventBus:
    """
    Publishes application events.

    Future implementations may publish to:
    - RabbitMQ
    - Kafka
    - Redis Streams
    - Azure Service Bus
    """

    @staticmethod
    def publish(event_name: str, payload: dict) -> None:

        logger.info(
            f"[EVENT] {event_name}: {payload}"
        )