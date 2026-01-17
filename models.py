from pydantic import BaseModel
class product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
    description: str
    
 
        
        
     