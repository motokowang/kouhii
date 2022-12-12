from fastapi import FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel, conint, constr
from collections import deque
from enum import Enum
from fastapi.testclient import TestClient
from mangum import Mangum
import os



def create_app() -> FastAPI:
    
    class Size(str, Enum):
        small = 'S'
        medium = 'M'
        large = 'L'
        
    class SmartCoffeeMachineJob(BaseModel):
        delay: conint(ge=0) = 0
        size: Size = Size.small
        grinder: conint(ge=1, le=10) = 1
    
        class Config:
            schema_extra = {
                'example': {
                    'delay': 0,
                    'size': Size.large,
                    'grinder': 5
                }
            }
        
    class SmartCoffeeMachine(BaseModel):
        __tablename__ = 'コーヒー'
        
        beans: conint(ge=0, le=100) = 100
        water: conint(ge=0, le=100) = 100
        job_queue: deque[SmartCoffeeMachineJob] = []
        
        def topoff_water(self):
            self.water = 100
            
        def topoff_beans(self):
            self.beans = 100
            
        def make_coffee(self, job: SmartCoffeeMachineJob):
            water_required: int = 0
            beans_required: int = 0
            
#            match job.size:
#                case Size.small:
#                    water_required = 10
#                    beans_required = 10
#                case Size.medium:
#                    water_required = 20
#                    beans_required = 20
#                case Size.large:
#                    water_required = 30
#                    beans_required = 30
                    
            if job.size == Size.small:
                water_required = 10
                beans_required = 10
            elif job.size == Size.medium:
                water_required = 20
                beans_required = 20
            elif job.size == Size.large:
                water_required = 30
                beans_required = 30
            else:
                raise HTTPException(status_code=400, detail='Choose S, M, or L -sized cups')
        

            if beans_required > self.beans or water_required > self.water:
                # Require more beans or water to complete job
                raise HTTPException(status_code=400, detail='Check hopper and water')
            else:
                self.water -= water_required
                self.beans -= beans_required
                self.job_queue.append(job)
            
    def get_levels():
        return {'beans': machine.beans, 'water': machine.water}
        
    
    app = FastAPI()
    machine = SmartCoffeeMachine()


    @app.get('/')
    async def root():
        return {'message': 'hello world'}


    @app.get('/levels')
    async def levels():
  
        '''GET /LEVELS

        Returns:
            beans: Integer from 0 to 100 representing the percentage level of coffee beans at the coffee machine reservoir. Where 0 means empty or 0% and 100 means full or 100%.
            water: Integer from 0 to 100 representing the percentage of the water tank level at
        '''
        # メタ.connect()
        return get_levels()
#        return {'beans': machine.beans, 'water': machine.water}
    
    
    @app.post('/brew')
    async def brew(job: SmartCoffeeMachineJob):
        '''POST /BREW

        • delay: Long integer from 0 representing the time in seconds to wait before running or brewing a coffee cup.
        • size: String representing the 3 coffee cup size options (S, M, L) to brew.
        • grinder: Integer to set ground coffee beans to use for brewing. From stronger coffee with fine (1) ground to lighter coffee with coarse (10) ground.

        Returns:
            _type_: _description_
        '''
        job_d = job.dict()
        job_d.update({'delay': job.delay,
                      'size': job.size,
                      'grinder': job.grinder})
        machine.make_coffee(job)
        return job_d
    
    
    @app.post('/maintenance')
    async def maintenance():
        '''POST /MAINTENANCE

        Tops off beans and water.
       
        Returns:
            _type_: _description_
        '''
        
        machine.topoff_beans()
        machine.topoff_water()
    
    return app
    
stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = create_app()
app = FastAPI(title="MyAwesomeApp", openapi_prefix=openapi_prefix) # Here is the magic