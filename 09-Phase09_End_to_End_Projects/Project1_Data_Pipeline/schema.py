from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class TransactionItem(BaseModel):
    product_id: str = Field(description="The internal SKU or product code")
    quantity: int = Field(description="Number of items purchased")
    unit_price_usd: float = Field(description="Price per single item in USD")

class CustomerRecord(BaseModel):
    customer_name: str = Field(description="Full extracted name of the customer")
    email: Optional[str] = Field(description="Email address, if present in the text")
    purchase_date: date = Field(description="Date of purchase in YYYY-MM-DD format")
    items: List[TransactionItem] = Field(description="List of all items purchased")
    total_value_usd: float = Field(description="Total transaction value in USD")
    is_flagged: bool = Field(description="True if the transaction mentions a return, complaint, or fraud suspected")
