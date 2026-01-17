from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column as C, Integer, String, Float, Boolean
Base = declarative_base()
class product(Base):
    
    __tablename__= "products"
    id= C(Integer, primary_key=True, index=True)                            
    name= C(String)
    price= C(Float)
    in_stock= C(Boolean)
    description= C(String)
    
    
 
        
        
     